from django.shortcuts import render, get_object_or_404

from main_app.models import VideoGroup
from .forms import PersonSettingsForm
from .tasks import start_parsing_celery


def settings(request):
    user = request.user
    settings = user.personsettings
    if request.method == 'POST':
        form = PersonSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
    else:
        form = PersonSettingsForm(instance=settings)
    return render(request, 'parser_service/settings.html', {'form': form})


def start_parsing(request):
    parsing_group_identifier = VideoGroup.objects.create()
    user_id = request.user.id
    video_group = VideoGroup.objects.order_by('-created_at')
    start_parsing_celery.delay(parsing_group_identifier.identifier, user_id)
    return render(request, 'main_app/parsed_data.html', {'identifiers': video_group, 'videos': []})