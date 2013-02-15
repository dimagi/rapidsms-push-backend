from django import forms

from threadless_router.backends.http.forms import BaseHttpForm


class PushForm(BaseHttpForm):
    Text = forms.CharField()
    MobileNumber = forms.CharField()

    def get_incoming_data(self):
        return {'identity': self.cleaned_data['MobileNumber'],
                'text': self.cleaned_data['Text']}
