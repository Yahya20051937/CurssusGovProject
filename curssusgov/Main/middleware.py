from django.http import HttpResponseForbidden


class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .models import Student
        # print(request.path)
        if request.path != '/Main/log_in/' and request.path != '/Admin/log_in/':
            if request.path.split('/')[1] == 'Main':
                student_serial_number = request.session.get('serial_number')
                if student_serial_number is None:
                    return HttpResponseForbidden('404')
            elif request.path.split('/')[1] == 'Admin':
                adminName = request.session.get('adminName')
                if adminName is None:
                    return HttpResponseForbidden('404 Admin')

        return self.get_response(request)
