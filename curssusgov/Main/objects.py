class ApplyingStudent:
    def __init__(self, application, coefficient):
        from .models import Course
        self.application = application
        self.student = application.student
        self.choices = [Course.objects.get(course_hash) for course_hash in application.chosen_courses_hashes.split('/'[:-1])]
        self.coefficient = coefficient
        self.score = self.calculate_score()

    def calculate_score(self):
        score = (self.student.ENN * .75 + self.student.ERN * 0.25) * self.coefficient
        return score

    def handle_admission(self, waiting_list):
        choice_number = 0
        for course in self.choices:
            choice_number += 1
            if course.available_seats > 0:
                # the students have a seat in this course
                self.application.admitted_in_choice = choice_number
                self.application.save()
                course.admitted_students.add(self)
                course.save()
                return
        # if we reach this line, the user hasn't been admitted in any of his choices
        waiting_list.append(self.application)




