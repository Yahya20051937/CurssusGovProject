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
    from .models import University, Application
    student = get_student(request)
    universities = University.objects.all()
    if university_hash is None:  # no space selected hash
        university = None
    else:
        university = University.objects.get(hash=university_hash)
    if university is not None:
        try:
            application = Application.objects.get(university=university, student=student)
        except Application.DoesNotExist:
            application = Application.objects.create(university=university,
                                                     student=student)  # the student access the university for the first time
            application.save()
            print(1)
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
    courses = [course for course in courses if course.hash not in student.all_chosen_courses_hashes.split('/')[
                                                                  :-1]]  # this to display only the course that are not chosen
    return render(request, 'Main/courses_page.html',
                  {'student': student, 'university': university, 'courses': courses, 'title': 'Courses'})


def add_course_to_choices(request, course_hash):
    from .functions import get_university, get_student
    student = get_student(request)
    university = get_university(request)
    if university is None:
        return HttpResponse("You must chose a university first")
    added = student.add_course_to_application_choices(university=university, course_hash=course_hash)
    if added:
        return get_university_courses(request)
    else:
        return HttpResponse("You have already added 10 courses to you choices")


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


def see_results(request):
    from .functions import get_university, get_student
    from .models import Application
    student = get_student(request)
    university = get_university(request)
    if university is None:
        return HttpResponse("You must chose a university first")
    if university.admission_processed:
        application = Application.objects.get(university=university, student=student)
        if application.admitted_in_choice != 0:
            request.session['admitted_in_course_hash'] = application.chosen_courses_hashes.split('/')[
                application.admitted_in_choice - 1]
        return render(request, 'Main/results_page.html',
                      {'student': student, 'university': university, 'application': application})
    return HttpResponse("The result are not yet processed")


def confirm_admission(request):
    from .models import Course, Application
    from .functions import get_university, get_student
    student = get_student(request)
    university = get_university(request)
    admitted_in_course_hash = request.session.get('admitted_in_course_hash')
    application = Application.objects.get(student=student, university=university)
    application.status = 'confirmed'
    application.save()
    if admitted_in_course_hash is None:
        return HttpResponse(404)
    course = Course.objects.get(hash=admitted_in_course_hash)
    course.confirmed_students.add(student)
    return redirect('/Main/results')


def upgrade_admission(request):
    from .models import Course, Application
    from .functions import get_university, get_student
    student = get_student(request)
    university = get_university(request)
    admitted_in_course_hash = request.session.get('admitted_in_course_hash')
    application = Application.objects.get(student=student, university=university)
    application.status = 'upgrading'
    application.save()
    if admitted_in_course_hash is None:
        return HttpResponse(404)
    course = Course.objects.get(hash=admitted_in_course_hash)
    course.upgrading_students.add(student)
    return redirect('/Main/results')




