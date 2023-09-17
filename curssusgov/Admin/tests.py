import random

from django.test import TestCase


# Create your tests here.
def admin():
    from Main.models import University, Course
    from .functions import get_random_hash
    universities_hashes = ["G4zg5ahz1CCZzOQQQxi", "y0VZKg20VoIOb8pTCeP"]
    fst_courses = ['MIP', 'BCG']
    fst_cities = ['FES', 'TANGER', 'MARRAKECH', 'MOHAMMADIA', 'STATT', 'HOCEIMA']
    est_cities = [
        "Casablanca",
        "Rabat",
        "Fes",
        "Marrakech",
        "Tangier",
        "Agadir",
        "Meknes",
        "Oujda",
        "Kenitra",
        "Nador",
        "Beni Mellal",
        "Tetouan",
        "Safi",
        "El Jadida",
        "Khouribga",
        "Settat",
        "Taza",
        "Mohammedia",
        "Khenifra",
        "Larache"
    ]
    est_courses = [
        "Génie Logiciel (Software Engineering)",
        "Informatique Industrielle (Industrial Computing)",
        "Réseaux et Télécommunications (Networks and Telecommunications)",
        "Conception de Systèmes Embarqués (Embedded Systems Design)",
        "Gestion de Projets Informatiques (Project Management in IT)",
        "Sécurité Informatique (Computer Security)",
        "Intelligence Artificielle (Artificial Intelligence)",
        "Ingénierie des Systèmes d'Information (Information Systems Engineering)",
        "Technologies Web Avancées (Advanced Web Technologies)",
        "Robotique et Automatisation (Robotics and Automation)"
    ]
    i = -1
    for uni in universities_hashes:
        i += 1
        uni_obj = University.objects.get(hash=uni)

        if i == 0:
            for city in fst_cities:
                for crs in fst_courses:
                    course = Course.objects.create(hash=get_random_hash(), city=city, subject=crs, university=uni_obj,
                                                   seats=760)
                    course.save()
        elif i == 1:
            for city in est_cities:
                for crs in est_courses:
                    course = Course.objects.create(hash=get_random_hash(), city=city, subject=crs, university=uni_obj,
                                                   seats=90)
                    course.save()


def test_admission_algorithm():
    from Main.models import Student, University, Course, Application
    students = list(Student.objects.all())
    Application.objects.all().delete()
    universities = list(University.objects.all())
    s = 0
    for student in students:
        s += 1
        print(s)
        for uni in universities:

            application = Application.objects.create(university=uni,
                                                     student=student)
            application.save()

            courses = list(Course.objects.filter(university=uni))
            courses_hashes = [c.hash for c in courses]
            for _ in range(10):
                course_hash = random.choice(courses_hashes)
                student.add_course_to_application_choices(university=uni, course_hash=course_hash)
                del courses_hashes[courses_hashes.index(course_hash)]


def test_confirmation_upgrade():
    from Main.models import Course, University, Application
    fst = University.objects.get(id=1)
    c = 0
    u = 0
    for course in Course.objects.all():
        admitted_students = list(course.admitted_students.all())
        for student in admitted_students:
            app = Application.objects.get(student=student, university=fst)

            if app.admitted_in_choice != 1:
                u += 1
                # course.students_to_upgrade.add(student)
                fst.upgrading_students.add(student)
                app.status = 'upgrading'
            else:
                s = random.choice([1, 2])
                if s == 1:
                    c += 1
                    course.enrolled_students.add(student)
                    course.admitted_students.remove(student)
                    app.status = 'confirmed'
                else:
                    app.status = 'rejected'
                    course.admitted_students.remove(student)

            app.save()

        course.save()
        fst.save()
        print(u, c)



def delete_all():
    from Main.models import Application, Course, University
    fst = University.objects.get(id=1)
    fst_courses = Course.objects.filter(university=fst)
    for c in fst_courses:
        c.admitted_students.clear()
        # c.students_to_upgrade.clear()
        c.enrolled_students.clear()
        c.save()

    for app in Application.objects.all():
        app.admitted_in_choice = 0
        app.status = 'sent'
        app.save()


def test():
    from Main.models import University
    delete_all()
    fst = University.objects.get(id=1)
    fst.admission_process()
    test_confirmation_upgrade()

