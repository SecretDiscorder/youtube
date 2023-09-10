from django.shortcuts import render
import pytube

def index(request):
    resolutions = ['360p', '720p', '1080p', '1440p', '2160p', 'mp3']
    title = ""
    streams = []
    streams3 = []
    error_message = ""

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        resolution = request.POST.get('resolution')

        if youtube_link and resolution:
            try:
                yt = pytube.YouTube(youtube_link)
                title = yt.title

                if resolution == 'mp3':
                    streams3 = yt.streams.filter(only_audio=True)
                else:
                    streams = yt.streams.filter(res=resolution)
            except pytube.exceptions.VideoUnavailable as e:
                error_message = f"Error: Video is unavailable ({str(e)})"
            except Exception as e:
                error_message = f"Error: {str(e)}"
        else:
            error_message = "Please enter a YouTube link and select a resolution."

    context = {
        'title': title,
        'streams': streams,
        'streams3': streams3,
        'resolutions': resolutions,
        'selected_resolution': resolution,
        'error_message': error_message,
    }

    return render(request, 'index.html', context)
