"""The schedule filtersets module."""

from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from professionals.filtersets import _get_professionals
from services.filtersets import _get_services

from .models import ProfessionalSchedule, ServiceSchedule


class ProfessionalScheduleFilterSet(filters.FilterSet):
    """The filter class for the professional schedule viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_("professional"),
        queryset=_get_professionals,
    )

    class Meta:
        """The metainformation."""

        model = ProfessionalSchedule
        fields = ("professional", "is_enabled", "day_of_week")


class ServiceScheduleFilterSet(filters.FilterSet):
    """The filter class for the service schedule viewset class."""

    service = filters.ModelChoiceFilter(
        label=_("service"),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = ServiceSchedule
        fields = ("service", "is_enabled", "day_of_week")
