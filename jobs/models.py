# jobs/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    link = models.URLField()
    company_name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')])
    salary_range = models.CharField(max_length=50, blank=True)
    experience_level = models.CharField(max_length=50, choices=[('Entry', 'Entry Level'), ('Mid', 'Mid Level'), ('Senior', 'Senior Level')], blank=True)
    skills_required = models.TextField(blank=True)  # New field for desired skills
    experience_required = models.TextField(blank=True)  # New field for experience requirements
    posted_date = models.DateField(default=timezone.now)  # New field for posted date

    def days_since_posted(self):
        return (timezone.now().date() - self.posted_date).days

    def __str__(self):
        return f"{self.title} at {self.company_name}"
    
    
# subscription
# class SubscriptionPlan(models.Model):
#     name = models.CharField(max_length=100)
#     duration_in_days = models.PositiveIntegerField()
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - {self.duration_in_days} days"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_in_days = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # New field for price

    def __str__(self):
        return f"{self.name} - {self.duration_in_days} days"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    has_access = models.BooleanField(default=False)  # Manually grant access

    def is_active(self):
        return self.has_access and self.end_date >= timezone.now()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_in_days)
        super().save(*args, **kwargs)