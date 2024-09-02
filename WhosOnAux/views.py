from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "WhosOnAux/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "WhosOnAux/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def user_home(request, user_id):
    return render(request, "WhosOnAux/user_home.html", {"user_id": user_id})

def attending(request, user_id):
    return render(request, "WhosOnAux/attending.html", {"user_id": user_id})

def party(request, user_id, party_id):
    return render(request, "WhosonAux/party.html", {"user_id": user_id, "party_id": party_id})

def hosting(request, user_id):
    return render(request, "WhosOnAux/hosting.html", {"user_id": user_id})

def dashboard(request, user_id, party_id):
    return render(request, "WhosOnAux/party_dashboard.html", {"user_id": user_id, "party_id": party_id})