from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    return HttpResponse(f"Você está na enquete {question_id}")


def results(request, question_id):
    response = "Você está olhando os resultados da enquete %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Você está votando em uma enquete %s." % question_id)