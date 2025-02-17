from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import Party, Attending
from .forms import NewPartyForm, InviteGuestForm

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
        filtered = Attending.objects.filter(attendee=user)
        parties = [entry.party for entry in filtered]
        context = {
            "user_id": user.id,
            "attending_parties": parties,
        }
        template = loader.get_template("WhosOnAux/attending.html")
        return HttpResponse(template.render(context, request))

    else:
        return redirect("landing")


def party(request, party_id):
    if request.user.is_authenticated:
        user = request.user
        party = Party.objects.get(id=party_id)

        # user is host, redirect to dashboard
        if user == party.host:
            return redirect('dashboard', party_id=party_id)

        # user is not host and is invited
        if Attending.objects.filter(party=party, attendee=user):
            context = {"party": party,
                       "user": user,
                       }
            template = loader.get_template("WhosOnAux/party.html")
            return HttpResponse(template.render(context, request))

        # user is not invited, redirect to list of parties they are attending
        else:
            # TODO: tell user they don'thave access to that party
            # TODO: allow user to request invite to party?
            return redirect('attending')

    else:
        return redirect("landing")


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
    if request.method == "POST":
        form = NewPartyForm(request.POST)
        if form.is_valid():
            host = request.user
            name = form.cleaned_data["party_name"]
            # TODO: date =
            description = form.cleaned_data["description"]
            new_party = Party(host=host, name=name, description=description)
            new_party.save()
            return redirect("hosting")
        else:
            raise Http404('invalid form!')
    # else:
    #     # for get requests, show an empty form
    #     form = NewPartyForm()
    # return render(request, "your_template.html", {"form": form})

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
    #TODO:  set up EMAIL_BACKEND in settings.py
    form = InviteGuestForm(request.POST)
    if form.is_valid():
        host = request.user
        # party = request.party get party name from request?
        #  get email from form
        # check if profile with email exists
        # if not, create profile
        # send email with link to create profile / accept invitation
        subject = f"{host} invitd you to a party"
        message = f"{host} has invited you to a party. Details of the invite with link to site"
        sent_from = 'snb331@nyu.edu'    # TODO: should be updated
        send_to = [form.cleaned_data["email"]]
        send_mail(subject, message, sent_from, send_to)
        return redirect("hosting")
    else:
        raise Http404('invalid form!')

