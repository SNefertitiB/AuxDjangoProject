from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse

from .models import Party, Attending
from .forms import NewPartyForm

# Create your views here.
def landing(request):
    return render(request, "WhosOnAux/landing.html")


def user_home(request):
    context = {'user_id': None}
    if request.user.is_authenticated:
        user_id = request.user.id
        context['user_id'] = user_id
        return render(request, "WhosOnAux/user_home.html", context)
    else:
        return redirect("landing")


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
    # TODO: get user from request.user
    # TODO: confirm user has access to party
    template = loader.get_template("WhosOnAux/party.html")
    party = Party.objects.get(id=party_id)
    context = {"party_id": party_id,
               "party_name": party.name,
               "description": party.description,
               }
    return HttpResponse(template.render(context, request))


def hosting(request):
    #TODO: redirect if user not logged in
    user_id = request.user.id
    parties = Party.objects.filter(host_id=user_id)                # <class 'django.db.models.query.QuerySet'>
    template = loader.get_template("WhosOnAux/hosting.html")
    context = {
        "hosting_parties": parties,
        "user_id": user_id
    }
    return HttpResponse(template.render(context, request))

def create_new_party(request):
    form = NewPartyForm(request.POST)
    if form.is_valid():
        host = request.user
        name = form.cleaned_data["party_name"]
        # TODO: date =
        description = form.cleaned_data["description"]
        new_party = Party(host=host, name=name, description=description)
        new_party.save()
        # TODO: fix redirect when trying to create new party (requires csrf token)
        return redirect("hosting")
    else:
        raise Http404('invalid form!')

def dashboard(request, party_id):
    # TODO: re-direct if user not logged in
    # TODO: re-direct if user is not host
    party = Party.objects.get(id=party_id)
    host = request.user
    invited = Attending.objects.filter(party=party)
    context = {"party": party,
               "host": host,
               "invited":invited,
               "yes":invited.filter(status='Y'),
               "no":invited.filter(status='N'),
               "maybe":invited.filter(status='M'),
               "no_response":invited.filter(status='NR'),
               }
    return render(request, "WhosOnAux/party_dashboard.html", context)