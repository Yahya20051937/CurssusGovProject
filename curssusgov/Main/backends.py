from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import Student
from Admin.models import Admin


class AbstractUserBackend(ModelBackend):
    def authenticate(self, request, serial_number=None, password=None, role=None, adminName=None, adminPassword=None, **kwargs):
        print(role)
        try:
            password_incorrect = False
            if role == 'student$':
                student = Student.objects.get(serial_number=serial_number)
                if student.password == password:
                    return student
                else:
                    password_incorrect = True
            elif role == 'admin$':
                admin = Admin.objects.get(adminName=adminName)
                if admin.adminPassword == adminPassword:
                    return admin
                else:
                    password_incorrect = True
            if password_incorrect:
                request.session['error'] = 'Password Incorrect'
                return None  # password is incorrect

        except ObjectDoesNotExist:
            if role == 'student$':
                request.session['error'] = 'Invalid Serial Number'
            else:
                request.session['error'] = 'Invalid adminName'
            return None  # serial number is not valid
