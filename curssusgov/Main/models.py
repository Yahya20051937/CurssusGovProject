from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


# Create your models here.
class Student(AbstractUser):
    serial_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, default='123')
    birth_date = models.DateField(max_length=30)
    ERN = models.FloatField()
    ENN = models.FloatField()
    ESN = models.FloatField()
    speciality = models.CharField(max_length=20, default='PC')
    school = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group, related_name='app_users')
    username = models.CharField(unique=False, max_length=20)
    user_permissions = models.ManyToManyField(Permission, related_name='app_users_permissions')
    role = 'student$'

    def add_course_to_application_choices(self, university, course_hash):
        student_choices = Application.objects.get(student=self, university=university)
        if len(student_choices.chosen_courses_hashes.split('/')[:-1]) < 10:
            student_choices.chosen_courses_hashes = student_choices.chosen_courses_hashes + f'{course_hash}/'
            student_choices.save()

    def get_university_application_choices(self, university):
        student_choices = Application.objects.get(student=self, university=university)
        courses_choices = []
        for course_hash in student_choices.chosen_courses_hashes.split('/')[:-1]:
            course = Course.objects.get(hash=course_hash)
            courses_choices.append(course)

        return courses_choices

    def change_course_position(self, university, new_position, course_hash):
        student_choices = Application.objects.get(student=self, university=university)
        student_choices.change_course_position(new_position=new_position, course_hash=course_hash)


class University(models.Model):
    name = models.CharField(max_length=20, default='')
    hash = models.CharField(max_length=20, unique=True)
    COEFFICIENTS = models.CharField(max_length=20)  # PC, SVT, MATH, ECONOMY (ORDER)

    def admission_process(self):
        from .objects import ApplyingStudent
        from .functions import quick_sort_applying_students
        # first get all the applications
        COEFFICIENTS = self.COEFFICIENTS.split(',')
        COEFFICIENTS_DICT = {'PC': float(COEFFICIENTS[0]), 'SVT': float(COEFFICIENTS[1]),
                             'MATH': float(COEFFICIENTS[2]), 'ECO': float(COEFFICIENTS[3])}
        applications = list(Application.objects.filter(university=self))
        applying_students = []
        for application in applications:
            applying_student = ApplyingStudent(application=application,
                                               coefficient=COEFFICIENTS_DICT[application.student.speciality])
            applying_students.append(applying_student)

        # Now we have to sort the students using the quick sort algorithm
        applying_students_sorted = quick_sort_applying_students(applying_students)
        waiting_list = []  # this list will the store the applications of the students who are not admitted
        # now for each student, for each one of his sorted choices, if there is a seat for him admit him and break
        for applyingStudent in applying_students_sorted:
            applyingStudent.handle_admission(waiting_list)


class Course(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, default=None)
    hash = models.CharField(max_length=20, default='')
    subject = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    seats = models.IntegerField()
    admitted_students = models.ManyToManyField(Student)

    # available seats = seats - admitted_students

    @property
    def available_seats(self):
        return self.seats - len(self.admitted_students.all())


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    chosen_courses_hashes = models.CharField(max_length=300)
    admitted_in_choice = models.IntegerField(default=0)

    def change_course_position(self, course_hash, new_position):
        chosen_courses_hashes = self.chosen_courses_hashes.split('/')[:-1]
        course_index = chosen_courses_hashes.index(course_hash)
        new_index = new_position - 1
        chosen_courses_hashes[course_index], chosen_courses_hashes[new_index] = chosen_courses_hashes[new_index], \
                                                                                chosen_courses_hashes[course_index]
        self.chosen_courses_hashes = ''
        for chosen_course in chosen_courses_hashes:
            self.chosen_courses_hashes += chosen_course
            self.chosen_courses_hashes += '/'
        self.save()
