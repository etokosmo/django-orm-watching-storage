from django.shortcuts import render

from datacenter.models import Passcard
from datacenter.models import Visit, is_visit_long, get_duration, format_duration


def passcard_info_view(request, passcode):
    this_passcard_visits_serialized = []

    passcard = Passcard.objects.get(passcode=passcode)
    this_passcard_visits = Visit.objects.filter(passcard=passcard)
    for visit in this_passcard_visits:
        this_passcard_visits_serialized.append(
            {
                'entered_at': visit.entered_at,
                'duration': format_duration(get_duration(visit)),
                'is_strange': is_visit_long(visit)
            }
        )

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits_serialized
    }
    return render(request, 'passcard_info.html', context)
