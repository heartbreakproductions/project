# from django.contrib import admin
# from .models import Program, Course, Semester, Subject

# @admin.register(Program)
# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'program')
#     list_filter = ('program',)
#     search_fields = ('name',)

# @admin.register(Semester)
# class SemesterAdmin(admin.ModelAdmin):
#     list_display = ('name', 'course')
#     list_filter = ('course',)
#     search_fields = ('name',)

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'semester')
#     list_filter = ('semester',)
#     search_fields = ('name',)
