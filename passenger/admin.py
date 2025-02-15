# from django.contrib import admin
# from .models import Passenger
# from django import forms

# class PassengerForm(forms.ModelForm):
#     class Meta:
#         model = Passenger
#         fields = '__all__'
#         widgets = {
#             'passport': forms.TextInput(attrs={'placeholder': 'XXXX XXXXXX'})
#         }


# @admin.register(Passenger)
# class PassengerAdmin(admin.ModelAdmin):
#     form = PassengerForm
#     list_display = ('user', 'first_name', 'last_name', 'phone_number', 'passport')
#     search_fields = ('user__username', 'first_name', 'last_name', 'passport')

from django.contrib import admin
from .models import Passenger
from django import forms

class PassengerForm(forms.ModelForm):
    
    class Meta:
        model = Passenger
        fields = '__all__'
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+7-XXX-XXX-XX-XX'}),
            'passport_series': forms.TextInput(attrs={'placeholder': 'XXXX'}),
            'passport_number': forms.TextInput(attrs={'placeholder': 'XXXXXX'})
        }


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    form = PassengerForm
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'passport_series', 'passport_number')
    search_fields = ('user__username', 'first_name', 'last_name', 'passport_series', 'passport_number')