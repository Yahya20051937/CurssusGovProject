from . import views

from django.urls import path

urlpatterns = [path("log_in/", views.log_in, name='log_in'),
               path("adminDashboard/", views.get_admin_dashboard, name='dashboard'),
               path("addStudentsTest/", views.add_students_test, name='add'),
               path("getStudentsDatabase/", views.get_students_database, name='db'),
               path("addUniversity/", views.add_university, name='university'),
               path("addCourse/", views.add_course, name='course'),
               path("startAdmissionProcess/", views.start_admission_process, name='admission'),
               path("stopConfirmingProcess/", views.stopConfirmingProcess, name='Stop'),
               path("startUpgradingProcess/", views.start_upgrading_process, name='upgrade'),
               ]