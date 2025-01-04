from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
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
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        filtered = Attending.objects.filter(attendee=user)
        parties = [entry.party for entry in filtered]
        context = {
            "user_id": user_id,
            "attending_parties": parties,
        }
        template = loader.get_template("WhosOnAux/attending.html")
        return HttpResponse(template.render(context, request))

    else:
        return redirect("landing")


def party(request, party_id):
    # TODO: confirm user has access to party
    template = loader.get_template("WhosOnAux/party.html")
    party = Party.objects.get(id=party_id)
    user = request.user
    context = {"party": party,
               "user": user,
               }
    return HttpResponse(template.render(context, request))


def hosting(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        parties = Party.objects.filter(host_id=user_id)                # <class 'django.db.models.query.QuerySet'>
        template = loader.get_template("WhosOnAux/hosting.html")
        context = {
            "hosting_parties": parties,
            "user_id": user_id
        }
        return HttpResponse(template.render(context, request))

    else:
        return redirect("landing")

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
    if request.user.is_authenticated:
        party = Party.objects.get(id=party_id)
        host = request.user

        if host != party.host:
            return redirect("party", party_id)   # view for guests

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

    else:
        return redirect("landing")


def invite_guest(request):
    form = NewPartyForm(request.POST)
    if form.is_valid():
        host = request.user
        #  get email from form
        # check if profile with email exists
        # if not, create profile
        # send email with link to create profile / accept invitation
        subject = "XYZ invitd you to ABC Party"
        message = f"{host} has invited you to a party. Details of the invite with link to site"
        sent_from = 'snb331@nyu.edu'    # TODO: should be updated
        send_mail(subject, message, sent_from)

        return None # TODO: update with redirect?