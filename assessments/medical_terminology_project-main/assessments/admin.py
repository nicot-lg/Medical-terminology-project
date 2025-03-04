from django.contrib import admin
from .models import Quiz, Question, Option
from django.utils.html import format_html


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz", "question_type", "image_preview")
    list_filter = ("quiz", "question_type")
    search_fields = ("question_text",)
    readonly_fields = ("image_preview",)  # Makes the image preview field non-editable

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url,
            )
        return "(No image)"

    image_preview.short_description = "Image Preview"


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("question", "option_text", "is_correct")
