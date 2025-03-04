from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, Question, Option


def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = 0
    total_questions = quiz.question_set.count()
    user_answers = {}

    if request.method == "POST":
        for question in quiz.question_set.all():
            if question.question_type == "MCQ":
                selected_option_id = request.POST.get(f"answer_{question.id}")
                selected_option = Option.objects.filter(id=selected_option_id).first()
                if selected_option and selected_option.is_correct:
                    score += 1
                user_answers[question.id] = (
                    selected_option.option_text if selected_option else "No answer"
                )

            elif question.question_type == "FIB":
                user_answer = (
                    request.POST.get(f"answer_{question.id}", "").strip().lower()
                )
                correct_answer = question.option_set.filter(
                    is_correct=True
                ).first()  # Use `option_set` here to get the correct answer
                if correct_answer and user_answer == correct_answer.option_text.lower():
                    score += 1
                user_answers[question.id] = user_answer

            elif question.question_type == "TF":
                user_answer = request.POST.get(f"answer_{question.id}")
                correct_option = question.option_set.filter(is_correct=True).first()
                if correct_option and user_answer == correct_option.option_text:
                    score += 1
                user_answers[question.id] = user_answer if user_answer else "No answer"

            elif question.question_type == "SA":
                user_answer = (
                    request.POST.get(f"answer_{question.id}", "").strip().lower()
                )
                correct_answer = question.option_set.filter(is_correct=True).first()
                if correct_answer and user_answer == correct_answer.option_text.lower():
                    score += 1
                user_answers[question.id] = user_answer

            elif question.question_type == "MQ":
                user_matches = []
                correct_matches = []
                for pair in question.option_set.all():
                    term, definition = pair.option_text.split("=")
                    user_input = request.POST.get(
                        f"match_answer_{question.id}_{pair.id}"
                    )
                    user_matches.append((term, user_input))
                    correct_matches.append((term, definition.strip()))

                if user_matches == correct_matches:
                    score += 1
                user_answers[question.id] = user_matches

            elif question.question_type == "OQ":
                user_order = [
                    request.POST.get(f"answer_{question.id}_{i}", "").strip()
                    for i in range(1, question.option_set.count() + 1)
                ]
                correct_order = [
                    option.option_text for option in question.option_set.all()
                ]
                if user_order == correct_order:
                    score += 1
                user_answers[question.id] = user_order

        percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

        return render(
            request,
            "assessments/quiz_results.html",
            {
                "quiz": quiz,
                "user_answers": user_answers,
                "score": score,
                "total_questions": total_questions,
                "percentage_score": percentage_score,
            },
        )

    return redirect("quiz_detail", quiz_id=quiz_id)


def home(request):
    return render(request, "assessments/home.html")


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "assessments/quiz_list.html", {"quizzes": quizzes})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    # Pre-process matching questions (if necessary)
    for question in questions:
        if question.question_type == "MQ":
            processed_options = []
            for option in question.option_set.all():
                # Split the term and definition in the view
                split_pair = option.option_text.split("=")
                if len(split_pair) == 2:
                    processed_options.append(
                        {"term": split_pair[0], "definition": split_pair[1]}
                    )
            question.processed_options = (
                processed_options  # Add processed options as a new attribute
            )

        # Add option count as an attribute for use in templates
        question.option_count = question.option_set.count()

    return render(
        request, "assessments/quiz_detail.html", {"quiz": quiz, "questions": questions}
    )
