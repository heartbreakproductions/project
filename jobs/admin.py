# jobs/admin.py
from django.contrib import admin
from .models import Country, State, City, Job, SubscriptionPlan, UserSubscription

class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'company_name', 'posted_date', 
        'job_type', 'experience_level', 'country', 'state', 'city'
    )
    list_filter = (
        'posted_date',          # Filter by posted date
        'job_type',             # Filter by job type (e.g., Full-time, Part-time)
        'experience_level',     # Filter by experience level (e.g., Entry, Mid, Senior)
        'country',              # Filter by country
        'state',                # Filter by state
        'city',                 # Filter by city
    )
    search_fields = ('title', 'company_name', 'description')
    date_hierarchy = 'posted_date'  # Adds date-based navigation for posted_date

# Register Job and other models
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Job, JobAdmin)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_in_days', 'price', 'description')  # Include price
    search_fields = ('name',)

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'has_access')
    list_filter = ('has_access', 'end_date')
    search_fields = ('user__username',)
    date_hierarchy = 'start_date'  # Adds date-based navigation for start_date

# Register SubscriptionPlan and UserSubscription with customized admin options
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)



# # jobs/admin.py
# from django.contrib import admin
# from .models import Country, State, City, Job, SubscriptionPlan, UserSubscription

# class JobAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 'company_name', 'posted_date', 
#         'job_type', 'experience_level', 'country', 'state', 'city'
#     )
#     list_filter = (
#         'posted_date',          # Filter by posted date
#         'job_type',             # Filter by job type (e.g., Full-time, Part-time)
#         'experience_level',     # Filter by experience level (e.g., Entry, Mid, Senior)
#         'country',              # Filter by country
#         'state',                # Filter by state
#         'city',                 # Filter by city
#     )
#     search_fields = ('title', 'company_name', 'description')
#     date_hierarchy = 'posted_date'  # Adds date-based navigation for posted_date

# # Register models with the admin site
# admin.site.register(Country)
# admin.site.register(State)
# admin.site.register(City)
# admin.site.register(Job, JobAdmin)

# class UserSubscriptionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'plan', 'start_date', 'end_date', 'has_access')
#     list_filter = ('has_access', 'end_date')
#     search_fields = ('user__username',)
#     date_hierarchy = 'start_date'  # Adds date-based navigation for start_date

# # Register SubscriptionPlan and UserSubscription with customized admin options
# admin.site.register(SubscriptionPlan)
# admin.site.register(UserSubscription, UserSubscriptionAdmin)
