from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment, Favorite, Vote, User
from django.contrib.auth.decorators import login_required
import os
import markdown
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.db import models
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.models import Notification
import re
from django.http import JsonResponse


# index
# show
# create
# edit
# update
# delete

        
@login_required  # Ensure user is logged in
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user is the author of the post
    if post.author != request.user:
        return redirect('posts:post_list')  # or raise a 403 Forbidden error

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Save the updated post. The model's save() method will handle old image deletion.
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form, 'post': post})



def post_list(request):
    # Get the sorting criteria from the query parameters (e.g., ?sort=most_commented)
    sort_by = request.GET.get('sort')

    # Annotate the posts with the number of comments, upvotes, and downvotes
    posts = Post.objects.annotate(
        num_comments=Count('post_comments', distinct=True),
        num_upvotes=Count('vote', filter=Q(vote__vote_type='upvote'), distinct=True),
        num_downvotes=Count('vote', filter=Q(vote__vote_type='downvote'), distinct=True)
    )

    # Sort the posts based on the sorting criteria
    if sort_by == 'most_commented':
        posts = posts.order_by('-num_comments')
    elif sort_by == 'most_upvotes':
        posts = posts.order_by('-num_upvotes')
    elif sort_by == 'most_downvotes':
        posts = posts.order_by('-num_downvotes')
    else:
        posts = posts.order_by('-id')  # Default sorting by creation date

    # Set up pagination
    paginator = Paginator(posts, 8)  # Show 3 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/post_list.html', {'posts': posts})



@login_required  # Ensure the user is logged in
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Convert the post body from Markdown to HTML
    post.body_html = markdown.markdown(post.body)

    # Check if the post is in the user's favorites
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    # Mark notifications as read for this post
    Notification.objects.filter(post=post, recipient=request.user, read=False).update(read=True)

    # Get all comments (including replies) related to this post
    # The 'parent' field is used to get nested replies.
    top_level_comments = post.post_comments.filter(parent=None)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'is_favorited': is_favorited,
        'top_level_comments': top_level_comments
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the current logged-in user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})



@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user is the author of the post
    if post.author != request.user:
        return redirect('posts:post_list')

    # Delete the image if it exists
    if post.image:
        old_image_path = post.image.path
        if os.path.isfile(old_image_path):
            os.remove(old_image_path)

    post.delete()
    return redirect('posts:post_list')





# @login_required
# def add_comment(request, post_id, parent_id=None):
#     post = get_object_or_404(Post, id=post_id)
#     parent_comment = None
#     initial_content = ''

#     if parent_id:
#         parent_comment = get_object_or_404(Comment, id=parent_id)
#         # Get the username of the parent comment author for replying
#         initial_content = f"@{parent_comment.user.username} "

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.post = post
#             if parent_comment:
#                 comment.parent = parent_comment

#             # Extract mentioned usernames from the comment content
#             mentioned_usernames = re.findall(r"@(\w+)", comment.content)
#             comment.save()

#             # Create a notification for each mentioned user
#             for mentioned_username in mentioned_usernames:
#                 mentioned_user = User.objects.filter(username=mentioned_username).first()
#                 if mentioned_user:
#                     Notification.objects.create(
#                         recipient=mentioned_user,
#                         notification_type='mention',
#                         post=post,
#                         comment=comment
#                     )

#             # Notification logic for post author and parent comment user
#             if post.author != request.user and not parent_comment:
#                 Notification.objects.create(
#                     recipient=post.author,
#                     notification_type='comment',
#                     post=post,
#                     comment=comment
#                 )
#             elif parent_comment and parent_comment.user != request.user:
#                 Notification.objects.create(
#                     recipient=parent_comment.user,
#                     notification_type='reply',
#                     post=post,
#                     comment=comment
#                 )

#             return redirect('posts:post_detail', post_id=post.id)
#     else:
#         # Pre-populate the form with @username if replying to a specific comment
#         form = CommentForm(initial={'content': initial_content})

#     return render(request, 'posts/comment_form.html', {'form': form, 'post': post, 'parent_comment': parent_comment})


@login_required
def add_comment(request, post_id, parent_id=None):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = None
    initial_content = ''

    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)
        # Get the username of the parent comment author for replying
        initial_content = f"@{parent_comment.user.username} "

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_comment:
                comment.parent = parent_comment

            # Extract mentioned usernames from the comment content
            mentioned_usernames = re.findall(r"@(\w+)", comment.content)
            comment.save()

            # Create a notification for each mentioned user
            for mentioned_username in mentioned_usernames:
                mentioned_user = User.objects.filter(username=mentioned_username).first()
                if mentioned_user and mentioned_user != request.user:  # Avoid notifying the author themselves
                    Notification.objects.create(
                        recipient=mentioned_user,
                        notification_type='mention',
                        post=post,
                        comment=comment
                    )

            # Notification logic for post author and parent comment user
            if post.author != request.user and not parent_comment:
                Notification.objects.create(
                    recipient=post.author,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            elif parent_comment and parent_comment.user != request.user:
                Notification.objects.create(
                    recipient=parent_comment.user,
                    notification_type='reply',
                    post=post,
                    comment=comment
                )

            return redirect('posts:post_detail', post_id=post.id)
    else:
        # Pre-populate the form with @username if replying to a specific comment
        form = CommentForm(initial={'content': initial_content})

    return render(request, 'posts/comment_form.html', {'form': form, 'post': post, 'parent_comment': parent_comment})










@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure that only the author can delete the comment
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    # Save the post ID before deleting the comment for redirection
    post_id = comment.post.id

    # Delete the comment
    comment.delete()

    return redirect('posts:post_detail', post_id=post_id)

# search

def post_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Filter posts by title or body containing the search query
        results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    return render(request, 'posts/post_search.html', {'results': results, 'query': query})


# save post
@login_required
def add_to_favorites(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Add the post to the user's favorites
    Favorite.objects.get_or_create(user=request.user, post=post)
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def remove_from_favorites(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Remove the post from the user's favorites
    Favorite.objects.filter(user=request.user, post=post).delete()
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def favorite_list(request):
    # Get all the posts saved in the user's favorites
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'posts/favorite_list.html', {'favorites': favorites})


@login_required
def vote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')

        if vote_type not in ['upvote', 'downvote']:
            return HttpResponseForbidden("Invalid vote type.")

        existing_vote = Vote.objects.filter(post=post, user=request.user).first()

        if existing_vote:
            if existing_vote.vote_type == vote_type:
                return JsonResponse({
                    'upvotes': post.upvotes,
                    'downvotes': post.downvotes
                })
            else:
                existing_vote.vote_type = vote_type
                existing_vote.save()

                if vote_type == 'upvote':
                    post.upvotes += 1
                    post.downvotes -= 1
                elif vote_type == 'downvote':
                    post.downvotes += 1
                    post.upvotes -= 1
        else:
            Vote.objects.create(post=post, user=request.user, vote_type=vote_type)

            if vote_type == 'upvote':
                post.upvotes += 1
            elif vote_type == 'downvote':
                post.downvotes += 1

        post.save()

        # Return updated vote counts as JSON
        return JsonResponse({
            'upvotes': post.upvotes,
            'downvotes': post.downvotes
        })

    return HttpResponseForbidden("Invalid request.")