from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.registration, name='registration'),
    path('home/', views.show_folders, name='home'),
    re_path('add/(?P<folder_id>[0-9]*)', views.add, name='add'),  # DEBUGGING: use <int:folder:id> instead of regex
    path('sets/', views.show_sets, name='sets'),
    path('del/', views.delete_folder, name='delete_folder'),
    path('questions/', views.show_questions, name='questions'),
    re_path('edit/add_q/(?P<set_id>[0-9]+)', views.add_question, name='add_question'),
    re_path('edit/del_q/(?P<question_id>[0-9]+)', views.del_question, name='del_question'),



    path('popup/', views.popup_test, name='popup'),
    path('edit/', views.edit, name='edit'),
    path('quiz_question/', views.quiz_question, name='quiz_question'),
    path('quiz_answer/', views.quiz_answer, name='quiz_answer'),
    path('result/', views.result, name='result'),
    path('logout/',  views.logout, name='logout'),
    # path('upload/', views.upload, name='upload'),
]
