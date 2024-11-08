from . import views
from django.urls import path

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='services_list'),
    # path('solved_assignments/programs/', views.program_list, name='program_list'),
    # path('solved_assignments/program/<int:program_id>/courses/', views.course_list, name='course_list'),
    # path('solved_assignments/course/<int:course_id>/semesters/', views.semester_list, name='semester_list'),
    # path('solved_assignments/semester/<int:semester_id>/subjects/', views.subject_list, name='subject_list'),
]