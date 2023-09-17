import time


class ApplyingStudent:
    def __init__(self, application, coefficient):

        self.application = application
        self.student = application.student
        self.student = application.student
        self.choices = self.get_choices()
        self.coefficient = coefficient
        self.score = self.calculate_score()

    def calculate_score(self):
        score = (self.student.ENN * .75 + self.student.ERN * 0.25) * self.coefficient
        return score

    def get_choices(self):
        from .models import Course
        choices = []
        chosen_courses_hashes = self.application.chosen_courses_hashes.split('/')[:-1]
        for course_hash in chosen_courses_hashes:
            course = Course.objects.get(hash=course_hash)
            choices.append(course)

        return choices

    def handle_admission(self, waiting_list):
        choice_number = 0

        for course in self.choices:

            choice_number += 1
            if course.available_seats > 0:
                # the students have a seat in this course
                self.application.admitted_in_choice = choice_number
                self.application.save()
                course.admitted_students.add(self.student)
                course.save()
                return

        # if we reach this line, the user hasn't been admitted in any of his choices
        print(';')
        waiting_list.append(self.student)

    def handle_upgrade(self):
        from .models import Application, Course
        choice_number = 1
        # the new choice should be bigger or equal to the student current choice
        # print(1, self.application.admitted_in_choice)
        while choice_number < self.application.admitted_in_choice:

            course = self.choices[choice_number]
            if course.available_seats > 0:
                # print(2)
                self.application.admitted_in_choice = choice_number
                self.application.save()
                course.admitted_students.add(self.student)
                course.save()
                for other_course in self.choices:
                    if other_course.hash != course.hash:  # since the student was admitted in this choice, he should free up his seat in all the other courses
                        if self.student.serial_number in [s.serial_number for s in
                                                          other_course.admitted_students.all()]:
                            course.admitted_students.remove(self.student)
                return
            else:
                # print(3)
                student_current_course_hash = self.choices[self.application.admitted_in_choice - 1].hash
                # print(3.1, student_current_course_hash)
                for student_to_upgrade in self.application.university.upgrading_students.all():
                    if student_to_upgrade.serial_number in [s.serial_number for s in course.admitted_students.all()]:
                        # we should get the self.student current course position for this student_to_upgrade
                        university = self.application.university
                        student_to_upgrade_application = Application.objects.get(university=university,
                                                                                 student=student_to_upgrade)
                        student_to_upgrade_choices_hashes = student_to_upgrade_application.chosen_courses_hashes.split(
                            '/')[
                                                            :-1]
                        # print(3.2, student_to_upgrade_choices_hashes)
                        # first if the self.student current course is in the  student to upgrade choices
                        if student_current_course_hash in student_to_upgrade_choices_hashes:
                            student_current_course_position_for_student_to_upgrade = student_to_upgrade_choices_hashes.index(
                                student_current_course_hash) + 1
                            # print(3.3, student_current_course_position_for_student_to_upgrade, student_to_upgrade_application.admitted_in_choice)
                            if student_current_course_position_for_student_to_upgrade < student_to_upgrade_application.admitted_in_choice:
                                # if this condition is True, then we can switch both students , and later we will try to find a better course for the student_to_upgrade
                                # print(4)
                                student_current_course = Course.objects.get(hash=student_current_course_hash)
                                print('c')
                                print(len(course.admitted_students.all()) + len(course.enrolled_students.all()))
                                print(len(student_current_course.admitted_students.all()) + len(
                                    student_current_course.enrolled_students.all()))

                                student_current_course.admitted_students.remove(self.student)
                                student_current_course.admitted_students.add(student_to_upgrade)
                                print('e', self.student.serial_number in [s.serial_number for s in student_current_course.admitted_students.all()])
                                print('f', student_to_upgrade.serial_number in [s.serial_number for s in course.admitted_students.all()])

                                course.admitted_students.remove(student_to_upgrade)
                                course.admitted_students.add(self.student)

                                course.save()
                                student_current_course.save()

                                self.application.admitted_in_choice = choice_number
                                self.application.save()
                                student_to_upgrade_application.admitted_in_choice = student_current_course_position_for_student_to_upgrade
                                student_to_upgrade_application.save()
                                print('d')
                                print(len(course.admitted_students.all()) + len(course.enrolled_students.all()))
                                print(len(student_current_course.admitted_students.all()) + len(
                                    student_current_course.enrolled_students.all()))
                                return

            choice_number += 1
