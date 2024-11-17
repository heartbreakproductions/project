from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from .models import UserProfile
import os
from posts.models import Post
from django.contrib.auth.models import User
import markdown

# @login_required
# def profile_view(request, username=None):
#     # If a username is provided in the URL, load that user's profile
#     if username:
#         user = get_object_or_404(User, username=username)
#     else:
#         user = request.user  # Default to the logged-in user's profile

#     # Fetch or create the UserProfile for this user
#     user_profile, created = UserProfile.objects.get_or_create(user=user)

#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=user)
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile_view', username=user.username)  # Redirect to the user's profile

#     else:
#         user_form = UserUpdateForm(instance=user)
#         profile_form = ProfileUpdateForm(instance=user_profile)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'user_profile': user_profile,
#         'user': user,  # Passing the user to the template
#     }
#     return render(request, 'accounts/profile.html', context)

# @login_required
# def profile_view(request):
#     user = request.user  # Automatically use the logged-in user

#     # Fetch or create the UserProfile for this user
#     user_profile, created = UserProfile.objects.get_or_create(user=user)

#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=user)
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('profile_view')  # Redirect to the user's profile

#     else:
#         user_form = UserUpdateForm(instance=user)
#         profile_form = ProfileUpdateForm(instance=user_profile)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'user_profile': user_profile,
#         'user': user,  # Passing the user to the template
#     }
#     return render(request, 'accounts/profile.html', context)

# def profile_view(request, username):
#     user = get_object_or_404(User, username=username)
#     user_profile = get_object_or_404(UserProfile, user=user)
#     return render(request, 'accounts/profile.html', {'user_profile': user_profile})


# def profile_view(request, username=None):
#     if not username:
#         return redirect('profile_view', username=request.user.username)

#     user = get_object_or_404(User, username=username)
#     user_profile = get_object_or_404(UserProfile, user=user)

#     # Convert markdown content to HTML (example markdown content)
#     markdown_content = user_profile.bio  # assuming 'bio' is a field with markdown text
#     user_profile.bio_html = markdown.markdown(markdown_content)

#     return render(request, 'accounts/profile.html', {'user_profile': user_profile})


# def profile_view(request, username=None):
#     if not username:
#         return redirect('profile_view', username=request.user.username)

#     user = get_object_or_404(User, username=username)
#     user_profile = get_object_or_404(UserProfile, user=user)

#     # Safely handle `None` by using an empty string as a fallback
#     markdown_content = user_profile.bio if user_profile.bio else ""
#     user_profile.bio_html = markdown.markdown(markdown_content)

#     return render(request, 'accounts/profile.html', {'user_profile': user_profile})


def profile_view(request, username=None):
    if not username:
        return redirect('profile_view', username=request.user.username)

    user = get_object_or_404(User, username=username)

    # Use get_or_create to avoid 404 errors if UserProfile doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Safely handle `None` by using an empty string as a fallback
    markdown_content = user_profile.bio if user_profile.bio else ""
    user_profile.bio_html = markdown.markdown(markdown_content)

    return render(request, 'accounts/profile.html', {'user_profile': user_profile})


@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect('profile_view', username=username)

    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view', username=username)
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    })



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save first and last name to the user instance
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            # Create UserProfile with additional fields
            phone_number = form.cleaned_data.get('phone_number')
            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                country=country,
                state=state
            )
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('posts:post_list')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/registration.html', {'form': form})

# @login_required
# def delete_account(request):
#     if request.method == "POST":
#         user = request.user

#         # Delete the user's profile image if it exists
#         if hasattr(user, 'userprofile') and user.userprofile.profile_image:
#             if os.path.isfile(user.userprofile.profile_image.path):
#                 os.remove(user.userprofile.profile_image.path)

#         # Delete all posts and their images associated with the user
#         user_posts = Post.objects.filter(author=user)  # Use 'author' instead of 'user'
#         for post in user_posts:
#             if post.image and os.path.isfile(post.image.path):
#                 os.remove(post.image.path)
#             post.delete()

#         # Delete the UserProfile
#         user.userprofile.delete()

#         # Delete the User
#         user.delete()

#         # Redirect to a suitable page after deletion
#         return redirect('home')

#     # If it's a GET request, show a confirmation page
#     return render(request, 'accounts/delete_account.html')


@login_required
def delete_account(request):
    user = request.user  # Ensure only logged-in user can delete their own account

    if request.method == "POST":
        # Delete the user's profile image if it exists
        if hasattr(user, 'userprofile') and user.userprofile.profile_image:
            if os.path.isfile(user.userprofile.profile_image.path):
                os.remove(user.userprofile.profile_image.path)

        # Delete all posts and their images associated with the user
        user_posts = Post.objects.filter(author=user)  # Use 'author' instead of 'user'
        for post in user_posts:
            if post.image and os.path.isfile(post.image.path):
                os.remove(post.image.path)
            post.delete()

        # Delete the UserProfile
        user.userprofile.delete()

        # Delete the User
        user.delete()

        messages.success(request, "Your account has been deleted.")
        return redirect('posts:post_list')  # Redirect to a suitable page after deletion

    # If it's a GET request, show a confirmation page
    return render(request, 'accounts/delete_account.html')
