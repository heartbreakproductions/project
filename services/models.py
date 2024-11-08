# from django.db import models

# class Program(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Course(models.Model):
#     program = models.ForeignKey(Program, related_name='courses', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Semester(models.Model):
#     course = models.ForeignKey(Course, related_name='semesters', on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.course.name} - {self.name}"

# class Subject(models.Model):
#     semester = models.ForeignKey(Semester, related_name='subjects', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name
