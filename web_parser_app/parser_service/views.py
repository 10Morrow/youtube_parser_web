from django.shortcuts import render, get_object_or_404
from .forms import PersonSettingsForm


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
    # video_group = VideoGroup.objects.create()
    # video_group_set = VideoGroup.objects.order_by('-created_at')
    # start_parse_data_for_id(video_group)
    # return render(request, 'main_app/video_list.html', {'identifiers': video_group_set, 'videos': []})
    return render(request, 'main_app/base.html')