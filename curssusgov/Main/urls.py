from . import views

from django.urls import path

urlpatterns = [path("log_in/", views.log_in, name='log_in'),
               path('home_page/', views.home, name='home'),
               path('home_page/<str:university_hash>/', views.home, name='home'),
               path('courses/', views.get_university_courses, name='courses'),
               path('add_course/<str:course_hash>/', views.add_course_to_choices, name='add'),
               path('choices/', views.get_choices, name='choices'),
               path('choices/<str:selected_course_hash>', views.get_choices, name='choices'),
               ]
