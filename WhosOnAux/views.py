from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render


from .models import Party
from .models import Attendees

# Create your views here.


def landing(request):
    return render(request, "WhosOnAux/landing.html")


def user_home(request, user_id):
    # TODO: 404 if user does not exist
    return render(request, "WhosOnAux/user_home.html", {"user_id": user_id})


def attending(request, user_id):
    # TODO: 404 if user does not exist
    # TODO: FIX THIS -- error loading parties -- something wrong with query
    # could also be something wrong with the model -- no __str__ attr
    # attending_query_set = Attendees.objects.filter(attendee=user_id)                # <class 'django.db.models.query.QuerySet'>
    # parties = [str(Party.objects.get(party_id=query.party_id)) for query in attending_query_set]
    parties = Attendees.objects.filter(attendee=user_id)
    context = {
        "user_id": user_id,
        "attending_parties": parties
    }
    template = loader.get_template("WhosOnAux/attending.html")
    return HttpResponse(template.render(context, request))


def party(request, user_id, party_id):
    return render(request, "WhosOnAux/party.html", {"user_id": user_id, "party_id": party_id})


def hosting(request, user_id):
    #TODO: 404 if user does not exist
    parties = Party.objects.filter(host_id=user_id)                # <class 'django.db.models.query.QuerySet'>
    template = loader.get_template("WhosOnAux/hosting.html")
    context = {
        "hosting_parties": parties,
        "user_id": user_id
    }
    return HttpResponse(template.render(context, request))


def dashboard(request, user_id, party_id):
    return render(request, "WhosOnAux/party_dashboard.html", {"user_id": user_id, "party_id": party_id})