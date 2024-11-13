from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Membership, Post, Comment, Vote
from .forms import GroupForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Count
from django.db.models import F
from django.db import models
from notifications.models import Notification
from django.contrib.auth.models import User
from .models import Post as GroupPost, Comment as GroupComment
from django.core.paginator import Paginator
import markdown
from django.utils.safestring import mark_safe
from notifications.utils import send_notification
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            group.members.add(request.user)  # Add owner as a member
            return redirect('groups:list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.method == 'POST':
        Membership.objects.get_or_create(user=request.user, group=group)
        return redirect('groups:group_detail', group_id=group.id)

    return render(request, 'groups/join_group.html', {'group': group})


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Remove the user's membership from the group
    Membership.objects.filter(user=request.user, group=group).delete()

    # Check if the group has no members left and delete it if necessary
    if group.members.count() == 0:
        group.delete()
        messages.success(request, f'The group "{group.name}" has been deleted because it has no members left.')
        return redirect('groups:list')

    messages.success(request, f'You have left the group "{group.name}".')
    return redirect('groups:group_detail', group_id=group.id)

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.owner == request.user:
        group.delete()
    return redirect('groups:list')



def group_list(request):
    sort_by = request.GET.get('sort_by', 'recent')
    search_query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)  # Get the page number from the request

    # Filter groups based on search query
    groups = Group.objects.all()
    if search_query:
        groups = groups.filter(name__icontains=search_query)

    # Sorting logic
    if sort_by == 'most_joined':
        groups = groups.annotate(num_members=models.Count('members')).order_by('-num_members')
    else:  # Default sorting by recent
        groups = groups.order_by('-created_at')

    # Pagination
    paginator = Paginator(groups, 10)  # Show 10 groups per page
    groups_page = paginator.get_page(page_number)

    return render(request, 'groups/group_list.html', {
        'groups': groups_page,
        'sort_by': sort_by,
        'search_query': search_query,
    })



def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Get the posts in the group
    posts = group.posts.all()

    # Handle sorting
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'upvotes':
        posts = posts.order_by('-upvotes')
    elif sort_by == 'downvotes':
        posts = posts.order_by('-downvotes')
    elif sort_by == 'comments':
        posts = posts.annotate(comment_count=models.Count('comments')).order_by('-comment_count')
    else:  # Default to recent
        posts = posts.order_by('-created_at')

    # Pagination
    paginator = Paginator(posts, 9)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    return render(request, 'groups/group_detail.html', {
        'group': group,
        'posts': posts_page,
        'sort_by': sort_by,
    })










@login_required
def create_post(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not Membership.objects.filter(user=request.user, group=group).exists():
        return HttpResponseForbidden("You must be a member of this group to create a post.")

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()

            # Notify group members about the new post
            members = Membership.objects.filter(group=group).exclude(user=request.user)
            for membership in members:
                Notification.objects.create(
                    recipient=membership.user,
                    notification_type='group_post',
                    group_post=post  # Link to the group post
                )

            return redirect('groups:group_detail', group_id=group.id)
    else:
        form = PostForm()

    return render(request, 'groups/create_post.html', {'form': form, 'group': group})




def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure the user is the author of the post
    if request.user != post.author:
        return redirect('groups:group_detail', group_id=post.group.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('groups:group_detail', group_id=post.group.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'groups/update_post.html', {'form': form, 'post': post})



def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure the user is the author of the post
    if request.user == post.author:
        post.delete()
    
    return redirect('groups:group_detail', group_id=post.group.id)



# @login_required
# def post_detail(request, post_id):
#     post = get_object_or_404(GroupPost, id=post_id)  # Use GroupPost
#     comments = post.comments.filter(parent=None)  # Get only top-level comments

#     # Check if the user has voted on this post
#     user_vote = post.group_votes.filter(user=request.user).first() if request.user.is_authenticated else None

#     if request.user.is_authenticated:
#         Notification.objects.filter(group_post=post, recipient=request.user, read=False).update(read=True)

#     return render(request, 'groups/post_detail.html', {
#         'post': post,
#         'top_level_comments': comments,
#         'user_vote': user_vote,
#     })
    


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)  # Use GroupPost
    comments = post.comments.filter(parent=None)  # Get only top-level comments

    # Convert the Markdown content to HTML
    post.body_html = mark_safe(markdown.markdown(post.body))

    # Check if the user has voted on this post
    user_vote = post.group_votes.filter(user=request.user).first() if request.user.is_authenticated else None

    if request.user.is_authenticated:
        Notification.objects.filter(group_post=post, recipient=request.user, read=False).update(read=True)

    return render(request, 'groups/post_detail.html', {
        'post': post,
        'top_level_comments': comments,
        'user_vote': user_vote,
    })



@login_required
def add_comment(request, post_id, parent_id=None):
    group_post = get_object_or_404(GroupPost, id=post_id)  # Retrieve the specific group post
    parent_comment = None
    initial_content = ''  # Used for pre-filling reply content

    if parent_id:
        # If `parent_id` is provided, this is a reply to an existing comment
        parent_comment = get_object_or_404(GroupComment, id=parent_id)
        initial_content = f"@{parent_comment.user.username} "

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = group_post
            if parent_comment:
                comment.parent = parent_comment  # Link to the parent comment if replying
            comment.save()

            # Send a notification to the parent comment author (if it's a reply)
            if parent_comment and parent_comment.user != request.user:
                Notification.objects.create(
                    recipient=parent_comment.user,
                    notification_type='group_comment_reply',
                    group_post=group_post,
                    group_comment=comment
                )

            # Notify the post author if it's a new top-level comment and they didn't write it
            elif not parent_comment and group_post.author != request.user:
                Notification.objects.create(
                    recipient=group_post.author,
                    notification_type='group_comment',
                    group_post=group_post
                )

            return redirect('groups:post_detail', post_id=post_id)

    else:
        form = CommentForm(initial={'content': initial_content})

    return render(request, 'groups/add_comment.html', {
        'form': form,
        'group_post': group_post,
        'parent_comment': parent_comment
    })















@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    post_id = comment.post.id  # Save the post ID to redirect back to the post
    comment.delete()
    return redirect('groups:post_detail', post_id=post_id)

# @login_required
# def upvote_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     vote, created = Vote.objects.get_or_create(user=request.user, post=post)

#     if created or vote.vote_type == 'downvote':
#         # If this is a new vote or changing from downvote to upvote
#         if vote.vote_type == 'downvote':
#             post.downvotes = F('downvotes') - 1  # Decrease downvotes
#         post.upvotes = F('upvotes') + 1  # Increase upvotes
#         vote.vote_type = 'upvote'  # Change vote type to upvote
#         vote.save()
#         post.save()

#     return redirect('groups:post_detail', post_id=post.id)

# @login_required
# def downvote_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     vote, created = Vote.objects.get_or_create(user=request.user, post=post)

#     if created or vote.vote_type == 'upvote':
#         # If this is a new vote or changing from upvote to downvote
#         if vote.vote_type == 'upvote':
#             post.upvotes = F('upvotes') - 1  # Decrease upvotes
#         post.downvotes = F('downvotes') + 1  # Increase downvotes
#         vote.vote_type = 'downvote'  # Change vote type to downvote
#         vote.save()
#         post.save()

#     return redirect('groups:post_detail', post_id=post.id)

@login_required
def upvote_post(request, post_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        vote, created = Vote.objects.get_or_create(user=request.user, post=post)

        if created or vote.vote_type == 'downvote':
            if vote.vote_type == 'downvote':
                post.downvotes = F('downvotes') - 1  # Decrease downvotes
            post.upvotes = F('upvotes') + 1  # Increase upvotes
            vote.vote_type = 'upvote'  # Change vote type to upvote
            vote.save()
            post.save()

        post.refresh_from_db()
        return JsonResponse({'success': True, 'new_upvote_count': post.upvotes, 'new_downvote_count': post.downvotes})

    return JsonResponse({'success': False})

@login_required
def downvote_post(request, post_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        vote, created = Vote.objects.get_or_create(user=request.user, post=post)

        if created or vote.vote_type == 'upvote':
            if vote.vote_type == 'upvote':
                post.upvotes = F('upvotes') - 1  # Decrease upvotes
            post.downvotes = F('downvotes') + 1  # Increase downvotes
            vote.vote_type = 'downvote'  # Change vote type to downvote
            vote.save()
            post.save()

        post.refresh_from_db()
        return JsonResponse({'success': True, 'new_upvote_count': post.upvotes, 'new_downvote_count': post.downvotes})

    return JsonResponse({'success': False})