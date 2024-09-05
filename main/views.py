from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from .models import Appointment, Doctor, Feedback, Speciality


def about(request):
    """ "Страница сведений о клинике и обратной связи"""
    if request.method == "POST":
        feedbak = Feedback.create(
            name=request.POST.get("review_name"),
            email=request.POST.get("review_email"),
            text=request.POST.get("review_text"),
            date=datetime.now(),
        )
        feedbak.save()
    return render(request, "main/about.html")


class DoctorsListView(ListView):
    """Показ списка врачей"""

    model = Doctor
    template_name = "main/doctors.html"

    def get_context(self):
        context_data = get_category_cache()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class AppointmentListView(ListView):
    """ "Показ списка всех записей на диагностику"""

    model = Appointment
    template_name = "main/appointments.html"

    def get_context(self):
        context_data = get_category_cache()
        return context_data

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = (
                    super()
                    .get_queryset()
                    .filter(date__gte=current_datetime)
                    .order_by(
                        "date",
                        "diagnostic",
                    )
                )
            else:  # для остальных пользователей
                queryset = (
                    super()
                    .get_queryset()
                    .filter(user=user, date__gte=current_datetime)
                    .order_by("date", "diagnostic")
                )
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentUserListView(ListView):
    """ "Показ списка забронированных пользователем записей на диагностику"""

    model = Appointment
    template_name = "main/user_appointments.html"

    def get_context(self):
        context_data = get_category_cache()
        return context_data

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            queryset = (
                super()
                .get_queryset()
                .filter(user=user, date__gte=current_datetime)
                .order_by("date")
            )
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentArchiveListView(ListView):
    """ "Показ списка прошедших записей на диагностику"""

    model = Appointment
    template_name = "main/appointments_archive.html"

    def get_context(self):
        context_data = get_category_cache()
        return context_data

    def get_queryset(self):
        user = self.request.user
        current_datetime = datetime.now()

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = (
                    super()
                    .get_queryset()
                    .filter(date__lt=current_datetime)
                    .order_by("-date", "diagnostic")
                )
            else:  # для остальных пользователей
                queryset = (
                    super()
                    .get_queryset()
                    .filter(user=user, date__lt=current_datetime)
                    .order_by("-date", "diagnostic")
                )
        else:  # для незарегистрированных пользователей
            queryset = None
        return queryset


class AppointmentAddView(View):
    """ "Запись пациента на диагностику"""

    success_url = reverse_lazy("main:user_appointments")

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.user = request.user
        appointment.save()
        return redirect(self.success_url)


class AppointmentCancelView(View):
    """ "Отмена записи на прием"""

    success_url = reverse_lazy("main:user_appointments")

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.user = None
        appointment.save()
        return redirect(self.success_url)


class SpecialityListView(ListView):
    """ "Показ списка всех специализаций"""

    model = Speciality
    template_name = "main/index.html"

    def get_context(self):
        context_data = get_category_cache()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset().order_by("title")
        return queryset


class SpecialityDetailView(DetailView):
    """ "Детальная информация о специализации"""

    model = Speciality

    def get(self, request, pk):
        speciality = Speciality.objects.get(id=pk)
        doctor = Doctor.objects.filter(speciality=speciality)
        context = {
            "speciality": speciality,
            "doctor": doctor,
            "title": f"{speciality.title}",
        }
        return render(request, "main/speciality.html", context)
