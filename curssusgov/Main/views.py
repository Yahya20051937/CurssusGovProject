from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .functions import get_student


# Create your views here.
def log_in(request):
    if request.method == "POST":
        serial_number = request.POST.get('serial_number')
        password = request.POST.get('password')

        student = authenticate(request=request, serial_number=serial_number, password=password, role='student$')

        if student is not None:
            login(request, student)
            request.session['serial_number'] = student.serial_number
            return redirect("/Main/home_page")

    return render(request, 'Main/log_in_page.html',
                  {'error': request.session.get('error'), 'user': 'student', 'action': '/Main/log_in/'})


def home(request, university_hash=None):  # if the code reaches this line, then the student is authenticated
    from .models import University
    student = get_student(request)
    universities = University.objects.all()
    if university_hash is None:  # no space selected hash
        university = None
    else:
        university = University.objects.get(hash=university_hash)
    if university is not None:
        request.session['university_hash'] = university_hash
    return render(request, "Main/home_page.html",
                  {"student": student, 'universities': universities, 'university': university})


def get_university_courses(request):
    from .models import Course
    from .functions import get_university
    student = get_student(request)
    university = get_university(request)
    if university is None:
        return HttpResponse("You must chose a university first")
    courses = list(Course.objects.filter(university=university))
    return render(request, 'Main/courses_page.html',
                  {'student': student, 'university': university, 'courses': courses, 'title': 'Courses'})


def add_course_to_choices(request, course_hash):
    from .functions import get_university, get_student
    student = get_student(request)
    university = get_university(request)
    if university is None:
        return HttpResponse("You must chose a university first")
    student.add_course_to_appplication_choices(university=university, course_hash=course_hash)
    return get_university_courses(request)


def get_choices(request, selected_course_hash=''):
    from .functions import get_university, get_student
    student = get_student(request)
    university = get_university(request)
    if university is None:
        return HttpResponse("You must chose a university first")
    university_choices = student.get_university_application_choices(university)
    if request.method == 'POST':
        new_position, course_hash = tuple(request.POST.get('new_position/course_hash').split('/'))
        student.change_course_position(new_position=int(new_position), course_hash=course_hash, university=university)
        request.method = 'GET'
        return get_choices(request)
    return render(request, 'Main/courses_page.html',
                  {'student': student, 'university': university, 'courses': university_choices, 'title': 'My choices',
                   'selected_course_hash': selected_course_hash, 'positions': range(1, len(university_choices) + 1)})


