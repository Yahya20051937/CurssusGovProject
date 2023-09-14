def get_student(request):
    from django.core.exceptions import ObjectDoesNotExist
    from .models import Student
    serial_number = request.session.get('serial_number')
    student = Student.objects.get(serial_number=serial_number)
    return student


def get_university(request):
    from .models import University
    university_hash = request.session.get('university_hash')
    if university_hash is None:
        return None
    else:
        university = University.objects.get(hash=university_hash)
        return university


def swap(array, index1, index2):
    array[index1], array[index2] = array[index2], array[index1]


def quick_sort_applying_students(applying_students_array):
    pivot = applying_students_array[-1]
    i = -1
    j = 0
    applying_students_number = len(applying_students_array)
    while j < applying_students_number:
        if applying_students_array[j].score < pivot.score:
            i += 1
            swap(applying_students_array, i, j)
        j += 1
    swap(applying_students_array, -1, i + 1)
    sub_array1 = applying_students_array[: i + 1]
    if len(sub_array1) > 1:
        sub_array1 = quick_sort_applying_students(sub_array1)
    sub_array2 = applying_students_array[i + 2:]
    if len(sub_array2) > 1:
        sub_array2 = quick_sort_applying_students(sub_array2)
    applying_students_array = sub_array1 + [pivot] + sub_array2
    return applying_students_array
