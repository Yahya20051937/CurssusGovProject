def get_admin(request):
    from .models import Admin
    adminName = request.session.get('adminName')
    admin = Admin.objects.get(adminName=adminName)
    return admin


def get_students():
    from Main.models import Student
    students = Student.objects.all()
    return list(students)


def get_random_hash():
    import string, random
    alphabet_symbols = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    numbers = list(string.digits)

    all_symbols_and_numbers = alphabet_symbols + numbers

    all_symbols_and_numbers = [t for t in all_symbols_and_numbers if t != '/']

    my_hash = ''
    for i in range(19):
        my_hash += all_symbols_and_numbers[random.randint(0, len(all_symbols_and_numbers) - 1)]
    return my_hash


