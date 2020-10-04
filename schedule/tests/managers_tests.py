"""The managers test module."""
from datetime import time

import arrow
import pytest
from django.db.models import QuerySet

from schedule.models import (AvailabilitySlot, ProfessionalClosedPeriod,
                             ProfessionalSchedule, ServiceClosedPeriod,
                             ServiceSchedule)

pytestmark = pytest.mark.django_db


def test_professional_schedule_manager_get_by_days(
        professional_schedules: QuerySet):
    """Should return schedules combined by weekdays."""
    professional = professional_schedules.first().professional
    schedules = ProfessionalSchedule.objects.get_by_days(professional)
    assert len(schedules[0]) == 2
    assert len(schedules[6]) == 0
    for schedule in schedules[1]:
        assert schedule.day_of_week == 1


def test_service_schedule_manager_get_by_days(service_schedules: QuerySet):
    """Should return schedules combined by weekdays."""
    service = service_schedules.first().service
    schedules = ServiceSchedule.objects.get_by_days(service)
    assert len(schedules[0]) == 2
    assert len(schedules[6]) == 0
    for schedule in schedules[1]:
        assert schedule.day_of_week == 1


def test_service_closed_periods_manager_get_overlapping_entries(
        service_closed_periods: QuerySet):
    """Should return overlapping closed periods."""
    manager = ServiceClosedPeriod.objects
    period = service_closed_periods.first()
    assert not manager.get_overlapping_entries(period).count()
    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    assert manager.get_overlapping_entries(period).count()

    period.start_datetime = arrow.utcnow().shift(days=+6).datetime
    period.end_datetime = arrow.utcnow().shift(days=+12).datetime
    assert manager.get_overlapping_entries(period).count()


def test_professional_closed_periods_manager_get_overlapping_entries(
        professional_closed_periods: QuerySet):
    """Should return overlapping closed periods."""
    manager = ProfessionalClosedPeriod.objects
    period = professional_closed_periods.first()
    assert not manager.get_overlapping_entries(period).count()
    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    assert manager.get_overlapping_entries(period).count()

    period.start_datetime = arrow.utcnow().shift(days=+6).datetime
    period.end_datetime = arrow.utcnow().shift(days=+12).datetime
    assert manager.get_overlapping_entries(period).count()


def test_professional_schedule_manager_get_overlapping_entries(
        professional_schedules: QuerySet):
    """Should return overlapping schedules."""
    manager = ProfessionalSchedule.objects
    schedule = professional_schedules.first()
    assert not manager.get_overlapping_entries(schedule).count()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()

    schedule.start_time = time(16)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()


def test_service_schedule_manager_get_overlapping_entries(
        service_schedules: QuerySet):
    """Should return overlapping schedules."""
    manager = ServiceSchedule.objects
    schedule = service_schedules.first()
    assert not manager.get_overlapping_entries(schedule).count()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()


def test_availability_slot_manager_get_overlapping_entries(
        availability_slots: QuerySet):
    """Should return overlapping slots."""
    manager = AvailabilitySlot.objects
    slot = availability_slots.first()
    assert not manager.get_overlapping_entries(slot).count()
    slot.start_datetime = arrow.utcnow().datetime
    slot.end_datetime = arrow.utcnow().shift(days=10).datetime
    assert manager.get_overlapping_entries(slot).count()


def test_availability_slot_manager_get_get_between_dates(
        availability_slots: QuerySet):
    """Should return slots between the dates."""
    professional = availability_slots.first().professional
    service = availability_slots.exclude(service__isnull=True).first().service
    manager = AvailabilitySlot.objects
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=10)

    result = manager.get_between_dates(start, end, professional)
    assert result.count() == 10
    assert result.first().professional == professional

    result = manager.get_between_dates(
        start,
        end,
        service.professional,
        service,
    )
    assert result.count() == 10
    assert result.first().service == service

    end = start.shift(days=100)
    result = manager.get_between_dates(start, end, professional)
    assert result.count() == 61
