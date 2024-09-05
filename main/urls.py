from django.urls import path

from main.apps import MainConfig

from .views import (AppointmentAddView, AppointmentArchiveListView,
                    AppointmentCancelView, AppointmentListView,
                    AppointmentUserListView, DoctorsListView,
                    SpecialityDetailView, SpecialityListView, about)

app_name = MainConfig.name

urlpatterns = [
    path("", SpecialityListView.as_view(), name="index"),
    path("about/", about, name="about"),
    path("doctors/", DoctorsListView.as_view(), name="doctors"),
    path("appointments/", AppointmentListView.as_view(), name="appointments"),
    path(
        "appointments/my/", AppointmentUserListView.as_view(), name="user_appointments"
    ),
    path(
        "appointments/archive/",
        AppointmentArchiveListView.as_view(),
        name="appointments_archive",
    ),
    path(
        "appointments/<int:pk>/add/",
        AppointmentAddView.as_view(),
        name="appointments_add",
    ),
    path(
        "appointments/<int:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointments_cancel",
    ),
    path(
        "speciality/<int:pk>/", SpecialityDetailView.as_view(), name="speciality_detail"
    ),
]
