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
    all_chosen_courses_hashes = models.CharField(max_length=1000,
                                                 default='')  # this attribute will be uses to display only the courses that are not chosen
    role = 'student$'

    def add_course_to_application_choices(self, university, course_hash):
        student_choices = Application.objects.get(student=self, university=university)
        if len(student_choices.chosen_courses_hashes.split('/')[:-1]) < 10:
            student_choices.chosen_courses_hashes = student_choices.chosen_courses_hashes + f'{course_hash}/'
            student_choices.save()
            self.all_chosen_courses_hashes = self.all_chosen_courses_hashes + f'{course_hash}/'
            self.save()
            return True
        return False

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
    name = models.CharField(max_length=20, unique=True)
    hash = models.CharField(max_length=20, unique=True)
    applying_finished = models.BooleanField(default=False)
    admission_processed = models.BooleanField(default=False)
    confirmation_finished = models.BooleanField(default=False)
    upgrading_students = models.ManyToManyField(Student, related_name='upgrading')
    waiting_list_students = models.ManyToManyField(Student, related_name='waitingList')
    COEFFICIENTS = models.CharField(max_length=20)  # PC, SVT, MATH, ECONOMY (ORDER)

    def getApplyingStudents(self, applications):
        from .objects import ApplyingStudent
        from .functions import quick_sort_applying_students
        COEFFICIENTS = self.COEFFICIENTS.split(',')
        COEFFICIENTS_DICT = {'PC': float(COEFFICIENTS[0]), 'SVT': float(COEFFICIENTS[1]),
                             'MATH': float(COEFFICIENTS[2]), 'ECO': float(COEFFICIENTS[3])}
        applying_students = []
        for application in applications:
            applying_student = ApplyingStudent(application=application,
                                               coefficient=COEFFICIENTS_DICT[application.student.speciality])
            applying_students.append(applying_student)

        # Now we have to sort the students using the quick sort algorithm
        applying_students_sorted = quick_sort_applying_students(applying_students)
        return applying_students_sorted

    def admission_process(self):
        from .objects import ApplyingStudent
        from .functions import quick_sort_applying_students
        # first get all the applications

        applications = list(Application.objects.filter(university=self))
        applyingStudentsSorted \
            = self.getApplyingStudents(applications=applications)  # (sorted)

        waiting_list = []  # this list will the store the applications of the students who are not admitted
        # now for each student, for each one of his sorted choices, if there is a seat for him admit him and break
        for applyingStudent in reversed(applyingStudentsSorted):
            print(applyingStudent.score)
            applyingStudent.handle_admission(waiting_list)

        self.admission_processed = True
        for student in waiting_list:
            self.waiting_list_students.add(student)
            self.save()
        self.save()

    def upgrading_process(self):

        # get the upgradingStudents applications
        applications = []
        for student in self.upgrading_students.all():
            application = Application.objects.get(student=student, university=self)
            applications.append(application)
        upgradingStudentsSorted = self.getApplyingStudents(applications=applications)
        for upgradingStudent in reversed(upgradingStudentsSorted):
            # print(upgradingStudent.score)
            print('a', upgradingStudent.application.admitted_in_choice)
            upgradingStudent.handle_upgrade()
            print('b', upgradingStudent.application.admitted_in_choice)
            print('-----------------------------------------------------------------------------')
        for course in list(Course.objects.filter(university=self)):
            print(len(course.enrolled_students.all()) + len(course.admitted_students.all()))


class Course(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, default=None)
    hash = models.CharField(max_length=20, default='')
    subject = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    seats = models.IntegerField()
    admitted_students = models.ManyToManyField(Student, related_name='admitted')
    enrolled_students = models.ManyToManyField(Student, related_name='enrolled')
    # available seats = seats - admitted_students

    @property
    def available_seats(self):
        return self.seats - (len(self.enrolled_students.all()) + len(
            self.admitted_students.all()))


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    chosen_courses_hashes = models.CharField(max_length=300)
    admitted_in_choice = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='sent')

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
