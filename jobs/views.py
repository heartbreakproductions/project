# jobs/views.py
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Job, UserSubscription, SubscriptionPlan
from .forms import JobSearchForm


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not authenticated

    # Check if the user has an active subscription with access
    user_subscription = UserSubscription.objects.filter(
        user=request.user,
        end_date__gte=timezone.now(),
        has_access=True
    ).first()

    if not user_subscription:
        return redirect('jobs:subscription_info')  # Redirect to subscription info if no active subscription

    # Proceed to display jobs
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.all().order_by('-posted_date')

    if form.is_valid():
        if form.cleaned_data['country']:
            jobs = jobs.filter(country=form.cleaned_data['country'])
        if form.cleaned_data['state']:
            jobs = jobs.filter(state=form.cleaned_data['state'])
        if form.cleaned_data['city']:
            jobs = jobs.filter(city=form.cleaned_data['city'])
        if form.cleaned_data['description']:
            jobs = jobs.filter(description__icontains=form.cleaned_data['description'])

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/job_list.html', {'form': form, 'page_obj': page_obj})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})


# def subscription_info(request):
#     plans = SubscriptionPlan.objects.all()  # Get all subscription plans
#     return render(request, 'jobs/subscription_info.html', {'plans': plans})

def subscription_info(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'jobs/subscription_info.html', {'plans': plans})