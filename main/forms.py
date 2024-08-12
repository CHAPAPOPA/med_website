from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    readonly_fields = ("doctor", "diagnostic")

    class Meta:
        model = Appointment
        fields = ("user",)
