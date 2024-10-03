from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .models import Party
# from .models import Attendees

# Create your views here.


def landing(request):
    return render(request, "WhosOnAux/landing.html")


def user_home(request):
    # TODO: 404 if user does not exist
    # TODO: get user_id from authorization
    context = {'user_id': None}
    if request.user.is_authenticated:
        user_id = request.user.id
        context['user_id'] = user_id

    return render(request, "WhosOnAux/user_home.html", context)


def attending(request):
    # TODO: 404 if user does not exist
    # i think error is because there are no users in the database
    user = request.user
    user_id = user.id
    # TODO: only show parties that user is attending
    parties = Party.objects.all()
    context = {
        "user_id": user_id,
        "attending_parties": parties,
    }
    template = loader.get_template("WhosOnAux/attending.html")
    return HttpResponse(template.render(context, request))


def party(request, party_id):
    # TODO: get user from rest.user
    # TODO: confirm user has access to party
    template = loader.get_template("WhosOnAux/party.html")
    party = Party.objects.get(party_id=party_id)
    context = {"party_id": party_id,
               "party_name": party.name,
               "description": party.description,
               }
    return HttpResponse(template.render(context, request))


def hosting(request):
    #TODO: 404 if user does not exist
    user_id = request.user.id
    parties = Party.objects.filter(host_id=user_id)                # <class 'django.db.models.query.QuerySet'>
    template = loader.get_template("WhosOnAux/hosting.html")
    context = {
        "hosting_parties": parties,
        "user_id": user_id
    }
    return HttpResponse(template.render(context, request))


def dashboard(request, party_id):
    party = Party.objects.get(party_id=party_id)
    context = {"user_id": request.user.id,
               "party_id": party_id,
               "party_name": party.name}
    return render(request, "WhosOnAux/party_dashboard.html", context)