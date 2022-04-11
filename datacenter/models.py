import datetime

from django.db import models
from django.utils import timezone

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit) -> datetime.timedelta:
    """Get duration between visit.leaved_at and visit.entered_at or visit.entered_at and now.time"""
    if visit.leaved_at:
        return visit.leaved_at - visit.entered_at
    now = timezone.localtime()
    entered_at_time = timezone.localtime(visit.entered_at)
    delta = now - entered_at_time
    return delta


def format_duration(duration: datetime.timedelta) -> str:
    """Format duration to '{hours}ч {minutes}мин'"""
    hours = get_hours_from_timedelta(duration)
    minutes = get_minutes_from_timedelta(duration)
    return f'{hours}ч {minutes}мин'


def is_visit_long(visit, minutes: int = 60) -> bool:
    """Check long visit"""
    if visit.leaved_at:
        visit_minutes = get_seconds_from_timedelta(visit.leaved_at - visit.entered_at) / SECONDS_IN_MINUTE
        return visit_minutes >= minutes
    visit_minutes = get_seconds_from_timedelta(get_duration(visit)) / SECONDS_IN_MINUTE
    return visit_minutes >= minutes


def get_minutes_from_timedelta(duration: datetime.timedelta) -> int:
    """From datetime.timedelta to minutes"""
    seconds = get_seconds_from_timedelta(duration)
    minutes = (seconds % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
    return int(minutes)


def get_hours_from_timedelta(duration: datetime.timedelta) -> int:
    """From datetime.timedelta to hours"""
    seconds = get_seconds_from_timedelta(duration)
    hours = seconds // SECONDS_IN_HOUR
    return int(hours)


def get_seconds_from_timedelta(duration: datetime.timedelta) -> int:
    """From datetime.timedelta to seconds"""
    seconds = duration.total_seconds()
    return int(seconds)
