from django.shortcuts import render
# from .models import Program, Course, Semester, Subject

# Create your views here.

def services_list(request):
    return render(request, 'services/services_list.html')

# # List of all programs
# def program_list(request):
#     programs = Program.objects.all()
#     return render(request, 'services/solved_assignments/program_list.html', {'programs': programs})

# # List of courses in a specific program
# def course_list(request, program_id):
#     program = get_object_or_404(Program, id=program_id)
#     courses = program.courses.all()
#     return render(request, 'services/solved_assignments/course_list.html', {'program': program, 'courses': courses})

# # List of semesters in a specific course
# def semester_list(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     semesters = course.semesters.all()
#     return render(request, 'services/solved_assignments/semester_list.html', {'course': course, 'semesters': semesters})

# # List of subjects in a specific semester with WhatsApp links
# def subject_list(request, semester_id):
#     semester = get_object_or_404(Semester, id=semester_id)
#     subjects = semester.subjects.all()
#     whatsapp_base_url = 'https://wa.me/YOUR_NUMBER?text='
#     return render(request, 'services/solved_assignments/subject_list.html', {'semester': semester, 'subjects': subjects, 'whatsapp_base_url': whatsapp_base_url})