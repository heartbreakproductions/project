# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import CommentForm
import markdown  # Add this import
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def blog_list(request):
#     blogs = Blog.objects.all().order_by('-created')
#     return render(request, 'blog/blog_list.html', {'blogs': blogs})

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created')
    
    # Set up pagination: 5 blogs per page (adjust as needed)
    paginator = Paginator(blogs, 5)  
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, year, month, day, slug):
    blog = get_object_or_404(
        Blog,
        slug=slug,
        status=Blog.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = blog.comments.all()

    # Convert the blog body from Markdown to HTML
    blog.body_html = markdown.markdown(blog.body)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog:blog_detail', year=year, month=month, day=day, slug=slug)  # Corrected here
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})

@login_required
def add_comment(request, year, month, day, slug):
    blog = get_object_or_404(
        Blog,
        slug=slug,
        status=Blog.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', year=year, month=month, day=day, slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the author of the comment
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    # Get the blog details for redirection
    blog = comment.blog
    comment.delete()

    return redirect('blog:blog_detail', year=blog.publish.year, month=blog.publish.month, day=blog.publish.day, slug=blog.slug)