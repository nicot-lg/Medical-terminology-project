import csv
from django.core.management.base import BaseCommand
from assessments.models import Quiz, Question, Option


class Command(BaseCommand):
    help = "Import questions and options from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to the CSV file to be imported"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Get or create the Quiz
                quiz, _ = Quiz.objects.get_or_create(title=row["quiz"])

                # Create the Question
                question, _ = Question.objects.get_or_create(
                    quiz=quiz,
                    question_text=row["question_text"],
                    question_type=row["question_type"],
                )

                # Add options based on the question type
                if question.question_type in ["MCQ", "TF", "MQ", "OQ"]:
                    options = row["options"].split(";")  # Split options by semicolon
                    correct_answers = row["correct_option"].split(
                        "|"
                    )  # Handle multiple correct answers if needed
                    for option_text in options:
                        is_correct = option_text.strip() in [
                            ans.strip() for ans in correct_answers
                        ]
                        Option.objects.create(
                            question=question,
                            option_text=option_text.strip(),
                            is_correct=is_correct,
                        )

                elif question.question_type == "FIB" or question.question_type == "SA":
                    # FIB (Fill in the Blank) or Short Answer questions
                    Option.objects.create(
                        question=question,
                        option_text=row["correct_option"].strip(),
                        is_correct=True,
                    )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
