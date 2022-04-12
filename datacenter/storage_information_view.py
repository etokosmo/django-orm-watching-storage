from django.shortcuts import render

from datacenter.models import Visit, get_duration, format_duration


def storage_information_view(request):
    non_closed_visits_serialized = []
    non_closed_visits = Visit.objects.filter(leaved_at__isnull=True)
    for visit in non_closed_visits:
        non_closed_visits_serialized.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': visit.entered_at,
                'duration': format_duration(get_duration(visit)),
            }
        )

    context = {
        'non_closed_visits': non_closed_visits_serialized,
    }
    return render(request, 'storage_information.html', context)
