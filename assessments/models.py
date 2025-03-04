from django.db import models
from django_ckeditor_5.fields import CKEditor5Field  # Import CKEditor5Field


class Quiz(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("MCQ", "Multiple Choice"),
        ("FIB", "Fill-in-the-Blank"),
        ("TF", "True/False"),
        ("SA", "Short Answer"),
        ("MQ", "Matching Questions"),
        ("OQ", "Ordering Questions"),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = CKEditor5Field(
        config_name="default"
    )  # Changed to CKEditor5Field for rich text
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    image = models.ImageField(
        upload_to="question_images/", blank=True, null=True
    )  # New field for images

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class StudentResponse(models.Model):
    student_name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        Option, on_delete=models.CASCADE, null=True, blank=True
    )
    response_text = models.TextField(
        blank=True, null=True
    )  # For short answer and fill-in-the-blank responses
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.question}"
