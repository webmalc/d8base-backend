"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

pytestmark = pytest.mark.django_db


def test_professional_schedule_post_save(
    professional_schedules: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_professional")
    schedule = professional_schedules.first()
    schedule.is_enabled = False
    schedule.save()

    assert generator.call_count == 1
    generator.assert_called_with(schedule.professional)


def test_professional_schedule_post_delete(
    professional_schedules: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_professional")
    schedule = professional_schedules.first()
    schedule.delete()

    assert generator.call_count == 1
    generator.assert_called_with(schedule.professional)


def test_service_schedule_post_save(
    service_schedules: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_service")
    schedule = service_schedules.first()
    schedule.is_enabled = False
    schedule.save()

    assert generator.call_count == 1
    generator.assert_called_with(schedule.service)


def test_service_schedule_post_delete(
    service_schedules: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_service")
    schedule = service_schedules.first()
    schedule.delete()

    assert generator.call_count == 1
    generator.assert_called_with(schedule.service)


def test_service_closed_period_post_save(
    service_closed_periods: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_service")
    closed_period = service_closed_periods.first()
    closed_period.is_enabled = False
    closed_period.save()

    assert generator.call_count == 1
    generator.assert_called_with(closed_period.service)


def test_service_closed_period_post_delete(
    service_closed_periods: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_service")
    closed_period = service_closed_periods.first()
    closed_period.delete()

    assert generator.call_count == 1
    generator.assert_called_with(closed_period.service)


def test_professional_closed_period_post_save(
    professional_closed_periods: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_professional")
    closed_period = professional_closed_periods.first()
    closed_period.is_enabled = False
    closed_period.save()

    assert generator.call_count == 1
    generator.assert_called_with(closed_period.professional)


def test_professional_closed_period_post_delete(
    professional_closed_periods: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_professional")
    closed_period = professional_closed_periods.first()
    closed_period.delete()

    assert generator.call_count == 1
    generator.assert_called_with(closed_period.professional)


def test_service_post_delete(
    services: QuerySet,
    mocker: MockFixture,
):
    """Should run the availability generator."""
    generator = mocker.patch("schedule.signals.generate_for_service")
    service = services.first()
    service.is_base_schedule = True
    service.save()

    assert generator.call_count == 0

    service.is_base_schedule = False
    service.save()

    assert generator.call_count == 1
    generator.assert_called_with(service)
