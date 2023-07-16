from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Video, VideoGroup


def video_identifiers_view(request):
    identifiers = VideoGroup.objects.order_by('-created_at')
    return render(request, 'main_app/parsed_data.html', {'identifiers': identifiers})


def settings(request):
    return render(request, 'main_app/settings.html')


def main_page_view(request):
    return render(request, 'main_app/main_page.html')


def return_playlist_by_id(request, identifier):
    video_group = VideoGroup.objects.order_by('-created_at')
    selected_identifier = get_object_or_404(VideoGroup, identifier=identifier)
    videos = Video.objects.all()
    filtered_videos = videos.filter(videogroup__identifier=selected_identifier) if selected_identifier else videos
    return render(request, 'main_app/video_list.html', {'identifiers': video_group, 'videos': filtered_videos})


def start_parsing(request):
    # video_group = VideoGroup.objects.create()
    # video_group = VideoGroup.objects.order_by('-created_at')
    # start_parse_data_for_id(video_group)
    # return render(request, 'main_app/video_list.html', {'identifiers': video_group, 'videos': []})
    return render(request, 'main_app/base.html')
