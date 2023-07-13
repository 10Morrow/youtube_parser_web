from django.http import HttpResponse
from django.shortcuts import render
from .models import Video, VideoGroup


def video_list_view(request):
    video_group = VideoGroup.objects.all()
    videos = Video.objects.all()
    selected_identifier = request.GET.get('identifier')
    filtered_videos = videos.filter(videogroup__identifier=selected_identifier) if selected_identifier else videos
    return render(request, 'main_app/video_list.html', {'identifiers': video_group, 'videos': filtered_videos})


def start_parsing(request):
    video_group = VideoGroup.objects.create()
    # start_parse_data_for_id(video_group)
    return render(request, 'main_app/video_list.html', {'identifiers': video_group, 'videos': filtered_videos})
