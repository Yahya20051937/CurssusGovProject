from datetime import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .functions import get_admin, get_students
import random


# Create your views here.
def log_in(request):
    if request.method == 'POST':
        adminName = request.POST.get('adminName')
        password = request.POST.get('password')

        admin = authenticate(request=request, adminName=adminName, adminPassword=password, role='admin$')
        if admin is not None:
            login(request, admin)
            request.session['adminName'] = adminName
            return redirect('/Admin/adminDashboard')
    return render(request, 'Main/log_in_page.html',
                  {'error': request.session.get('error'), 'user': 'admin', 'action': '/Admin/log_in/'})


def get_admin_dashboard(request):
    admin = get_admin(request)
    return render(request, 'Admin/base2.html', {'admin': admin})


def get_students_database(request):
    admin = get_admin(request)
    students = get_students()
    return render(request, 'Admin/studentsDatabasePage.html', {'admin': admin, 'students': students})


def add_students_test(request):
    from faker import Faker
    from Main.models import Student
    schools = ['Hill Academy Education Center', 'Hill Charter Education Center', 'East International School',
               'Central Community Education Center', 'Hill Secondary School', 'North Secondary Academy',
               'River Academy Academy', 'Lake Academy Institute', 'North Middle Academy',
               'South Primary Education Center', 'Lake Technical Education Center', 'River Elementary Institute',
               'North Elementary Education Center', 'City Academy Education Center', 'River Academy Education Center',
               'Valley Secondary School', 'West Technical Academy', 'North Academy Education Center',
               'Valley Secondary Academy', 'Hill International Academy', 'South Secondary Education Center',
               'North Charter Institute', 'Valley Academy Institute', 'South Elementary School',
               'East Technical Education Center', 'North International Academy', 'South Community Institute',
               'Central Secondary Institute', 'Lake Academy Education Center', 'East Primary Academy',
               'West Secondary Academy', 'Central Middle Academy', 'Hill Middle Academy', 'Lake Secondary School',
               'City Elementary Academy', 'Central Technical Institute', 'South Technical Academy', 'River High School',
               'North Secondary Education Center', 'Lake Primary Education Center', 'East Charter School',
               'East High Institute', 'West Secondary Education Center', 'Hill Middle Education Center',
               'North Community School', 'West International School', 'Valley High Education Center',
               'North Technical Institute', 'River Community School', 'North Primary Institute',
               'Valley Charter School', 'Hill Technical Education Center', 'Central Elementary School',
               'Lake Secondary Academy', 'Hill Technical Institute', 'Central Secondary School',
               'Central Technical Academy', 'Lake Middle School', 'River Middle Academy',
               'Central International Academy', 'West Secondary Institute', 'Hill Elementary Academy',
               'South High Education Center', 'South Academy School', 'Lake Primary Academy',
               'Valley International Education Center', 'North High Academy', 'East High Academy',
               'Central Elementary Academy', 'Hill Primary School', 'South Charter Academy', 'Hill Community Academy',
               'City Elementary School', 'West International Education Center', 'East Community Education Center',
               'Lake Elementary Academy', 'South Academy Education Center', 'Lake High School',
               'South Technical School', 'West Charter Education Center', 'River Secondary School',
               'North Community Academy', 'City Charter Academy', 'Lake Secondary Education Center',
               'Hill Charter School', 'North Secondary Institute', 'East Elementary Education Center',
               'Valley Technical Education Center', 'West Technical School', 'South High School',
               'South Charter School', 'Central High Institute', 'Lake International Education Center',
               'Hill Academy School', 'North Primary Academy', 'Central International Education Center',
               'City Secondary Education Center', 'South Technical Institute', 'South Elementary Academy',
               'River Primary Academy', 'South Community Academy', 'North Technical Education Center',
               'Hill Primary Education Center', 'West Technical Institute', 'City Primary School',
               'East Primary Institute', 'Lake Charter Academy', 'River High Institute', 'East International Institute',
               'East High School', 'Hill Elementary School', 'Hill Middle Institute', 'Valley Primary Academy',
               'Lake Middle Education Center', 'Lake Technical School', 'River International Academy',
               'Hill High School', 'Hill Community Institute', 'North Middle Education Center', 'West Secondary School',
               'Central Charter School', 'River Middle Education Center', 'North Secondary School',
               'East Middle Institute', 'West High Academy', 'North High School', 'West Middle School',
               'Hill International School', 'River Middle School', 'Central Academy Institute',
               'Hill Technical Academy', 'River Charter Academy', 'North Charter Academy', 'Hill Charter Institute',
               'Central Middle Institute', 'West Primary Education Center', 'Valley High Academy',
               'East Middle Education Center', 'North International Institute', 'City Elementary Institute',
               'Hill Secondary Education Center', 'River High Education Center', 'West Community Academy',
               'Hill Community Education Center', 'South Middle School', 'West Charter Academy',
               'East Charter Institute', 'West Community School', 'Valley Elementary Education Center',
               'South High Academy', 'West Community Education Center', 'Central Elementary Institute',
               'Hill Elementary Institute', 'Central Middle Education Center', 'Valley Elementary Academy',
               'East Technical School', 'Valley Community Academy', 'East Secondary Institute',
               'City Charter Education Center', 'North Community Institute', 'Hill Primary Academy',
               'East Primary School', 'East Academy Academy', 'Lake Technical Institute', 'City Primary Academy',
               'North Academy School', 'South Middle Education Center', 'City Community Institute',
               'Valley Secondary Institute', 'East Elementary Academy', 'South International Education Center',
               'Lake High Institute', 'North Academy Academy', 'Valley Charter Institute', 'River Technical School',
               'River Community Academy', 'East Community Institute', 'Valley Primary School',
               'Valley Charter Education Center', 'River Primary Institute', 'South Elementary Institute',
               'West Primary School', 'West High School', 'Central International School', 'City Charter School',
               'South Elementary Education Center', 'Valley Middle Academy', 'Central High Academy',
               'River Primary School', 'Valley Academy School', 'North Academy Institute',
               'Lake Elementary Education Center', 'City High School', 'City Elementary Education Center',
               'Valley Elementary Institute', 'City Academy School', 'Lake Community Institute',
               'Hill Technical School', 'City Middle Institute', 'Lake Charter School', 'Hill High Institute',
               'City Academy Academy', 'East High Education Center', 'East Technical Academy',
               'South Secondary Academy', 'Hill High Academy', 'South Community Education Center',
               'West Primary Institute', 'City High Academy', 'City Academy Institute', 'East Community Academy',
               'East Secondary Academy', 'West Elementary Education Center', 'Hill High Education Center',
               'South Primary Institute', 'South International Academy', 'Valley International School',
               'Lake Academy Academy', 'Lake Community Education Center', 'Central Community Academy',
               'Lake International Institute', 'Central Primary Academy', 'North Middle School',
               'Central Primary School', 'City Technical Institute', 'East Technical Institute',
               'City Secondary Institute', 'East Academy Education Center', 'City International Education Center',
               'River Secondary Academy', 'Valley Community School', 'Valley Technical Academy',
               'Hill Community School', 'West Academy Institute', 'Hill Middle School',
               'Central Primary Education Center', 'Valley Technical School', 'Central Technical School',
               'Valley Academy Academy', 'Lake Elementary Institute', 'East International Academy',
               'River International School', 'West International Academy', 'Central Academy School',
               'City Community Education Center', 'River International Education Center',
               'Valley Primary Education Center', 'City Charter Institute', 'Hill Academy Institute',
               'North Elementary School', 'City Community School', 'West Primary Academy', 'North Middle Institute',
               'River High Academy', 'Valley International Institute', 'City Technical Academy',
               'Central Charter Institute', 'City Primary Education Center', 'Valley High School',
               'Lake Secondary Institute', 'Valley Charter Academy', 'Lake Technical Academy',
               'City International School', 'North Elementary Institute', 'East Secondary School', 'City Middle School',
               'River Primary Education Center', 'Central Technical Education Center',
               'Valley Academy Education Center', 'City Primary Institute', 'South Middle Academy',
               'River Academy Institute', 'West Academy Academy', 'Valley Primary Institute', 'River Charter School',
               'West Community Institute', 'River Charter Institute', 'River Academy School',
               'Hill International Institute', 'River International Institute', 'City High Institute',
               'East Academy School', 'East Primary Education Center', 'South Charter Education Center',
               'South High Institute', 'South Charter Institute', 'City International Academy',
               'Valley International Academy', 'Central Secondary Education Center', 'Lake Community School',
               'River Elementary Education Center', 'Lake Primary School', 'City International Institute',
               'Lake High Education Center', 'Hill Secondary Academy', 'Valley High Institute',
               'North Primary Education Center', 'River Technical Academy', 'Central Academy Education Center',
               'North Elementary Academy', 'Central Charter Education Center', 'Central Community Institute',
               'East Community School', 'River Community Institute', 'Central Charter Academy',
               'City High Education Center', 'Valley Secondary Education Center', 'North Technical Academy',
               'Valley Community Institute', 'Valley Middle School', 'River Elementary School',
               'Central High Education Center', 'West Technical Education Center', 'River Community Education Center',
               'West Charter School', 'City Middle Education Center', 'River Elementary Academy',
               'Hill Primary Institute', 'Central Primary Institute', 'Hill Secondary Institute',
               'North High Education Center', 'City Technical Education Center', 'South Community School',
               'Lake Charter Institute', 'City Secondary School', 'West High Education Center',
               'North International School', 'Hill Charter Academy', 'East Secondary Education Center',
               'East Elementary School', 'South Academy Institute', 'North Community Education Center',
               'North Primary School', 'Lake Middle Institute', 'City Community Academy', 'West Charter Institute',
               'Lake Charter Education Center', 'Hill Elementary Education Center', 'South Secondary School',
               'Lake High Academy', 'Central Community School', 'North International Education Center',
               'Central Secondary Academy', 'Central Middle School', 'Valley Middle Education Center',
               'East Middle School', 'East Middle Academy', 'Central Academy Academy', 'North Charter Education Center',
               'Valley Technical Institute', 'Valley Elementary School', 'Valley Community Education Center',
               'River Middle Institute', 'West Middle Institute', 'North Technical School', 'South Primary School',
               'East Charter Education Center', 'Valley Middle Institute', 'North High Institute',
               'East Charter Academy', 'South Primary Academy', 'West Academy Education Center', 'City Middle Academy',
               'West Academy School', 'West Middle Academy', 'City Technical School', 'South International School',
               'West Elementary Institute', 'West Middle Education Center', 'West International Institute',
               'Hill Academy Academy', 'East Elementary Institute', 'Lake Primary Institute', 'Lake Academy School',
               'River Technical Institute', 'City Secondary Academy', 'North Charter School', 'East Academy Institute',
               'River Charter Education Center', 'West High Institute', 'Lake Middle Academy',
               'West Elementary Academy', 'Central High School', 'West Elementary School',
               'East International Education Center', 'Central International Institute', 'South Secondary Institute',
               'Lake International School', 'South Academy Academy', 'River Secondary Education Center',
               'River Technical Education Center', 'South Middle Institute', 'River Secondary Institute',
               'Hill International Education Center', 'Lake Community Academy', 'Lake Elementary School',
               'South Technical Education Center', 'Central Elementary Education Center', 'Lake International Academy',
               'South International Institute']
    moroccan_cities = [
        "Casablanca",
        "Marrakech",
        "Rabat",
        "Fes",
        "Tangier",
        "Agadir",
        "Meknes",
        "Oujda",
        "Kenitra",
        "Tetouan",
        "Safi",
        "Mohammedia",
        "Khouribga",
        "El Jadida",
        "Beni Mellal",
        "Nador",
        "Errachidia",
        "Taza",
        "Settat",
        "Larache",
        "Ksar El Kebir",
        "Guelmim",
        "Berrechid",
        "Tifelt",
        "Taourirt",
        "Essaouira", "Al Hoceima",
        "Lagouira",
        "Tan-Tan",
        "Figuig",
        "Smara",
        "El Kelaa des Sraghna",
        "Sidi Kacem",
        "Tiznit",
        "Larache",
        "Ksar El Kebir",
        "Guelmim",
        "Berrechid",
        "Tifelt",
        "Taourirt",
        "Essaouira",
        "Al Hoceima",
        "Lagouira",
        "Tan-Tan",
        "Figuig",
        "Smara",
        "El Kelaa des Sraghna",
        "Sidi Kacem",
        "Tiznit",
        "Azrou",
        "Midelt",
        "Dakhla",
        "Berkane",
        "Sefrou"]
    fake = Faker()

    # 10000
    for i in range(10000):
        print(i)
        first_name = fake.first_name()
        last_name = fake.last_name()
        year = random.choice([2005, 2006])
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 27))
        birth_date = datetime(year=year, day=day, month=month)
        ERN = float(f'{random.randint(10, 19)}.{random.randint(0, 99)}')
        ENN = float(f'{random.randint(10, 19)}.{random.randint(0, 99)}')
        ESN = float(f'{random.randint(10, 19)}.{random.randint(0, 99)}')
        school = random.choice(schools)
        city = random.choice(moroccan_cities)
        serial_number = 'N'
        for _ in range(30):
            serial_number += str(random.randint(0, 9))
        student = Student.objects.create(serial_number=serial_number, first_name=first_name, last_name=last_name,
                                         birth_date=birth_date, ERN=ERN, ENN=ENN, school=school, city=city, ESN=ESN)
        student.save()
    return get_students_database(request)


def add_university(request):
    from .functions import get_random_hash
    from Main.models import University
    if request.method == "POST":
        name = request.POST.get('name')
        university = University.objects.create(name=name, hash=get_random_hash(), COEFFICIENTS='1.2,1.4,1.0,0.0')
        university.save()
        request.method = 'GET'
        return add_university(request)
    return render(request, 'Admin/addUniversityPage.html')  ############ Create admin


def add_course(request):
    from .functions import get_random_hash
    from Main.models import University, Course
    universities = University.objects.all()
    if request.method == "POST":
        university_hash = request.POST.get('')
        university = University.objects.get(hash=university_hash)
        subject = request.POST.get('subject')
        seats = int(request.POST.get('seats'))
        city = request.POST.get('city')
        course = Course.objects.create(university=university, subject=subject, hash=get_random_hash(), seats=seats,
                                       city=city)
        course.save()
        request.method = "GET"
        return add_university(request)
    return render(request, 'Admin/addCoursePage.html', {'universities': universities})


def start_admission_process(request):
    from Main.models import University
    admin = get_admin(request)
    if request.method == "POST":
        university_hash = request.POST.get('university')
        university = University.objects.get(hash=university_hash)
        university.admission_process()
        return get_admin_dashboard(request)
    return render(request, 'Admin/startAdmissionProcessPage.html', {'admin': admin, 'universities':University.objects.all()})


def start_upgrading_process(request):
    pass



