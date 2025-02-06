from django import forms

class NewPartyForm(forms.Form):
    party_name = forms.CharField(label="party_name", max_length=200)
    description = forms.CharField(label="description", max_length=500)
    # date

class InviteGuestForm(forms.Form):
    email = forms.CharField(label='email', max_length=200)
