from youtube_dl import YoutubeDL as yd

info_dict = ydl.extract_info("https://www.youtube.com/watch?v=MhQKe-aERsU", download=False)
video_url = info_dict.get("url", None)
video_id = info_dict.get("id", None)
video_title = info_dict.get('title', None)

print(video_title)
print(video_id)
print(video_id)
print(info_dict)