from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_list, name="quiz_list"),
    path("<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path(
        "<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"
    ),  # URL for quiz submission
]
