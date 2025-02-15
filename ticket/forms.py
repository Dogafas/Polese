from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['voyage', 'passenger', 'departure_stop', 'arrival_stop', 'price', 'status'] 