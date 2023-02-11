from django import forms
# from django.db import ModelForm
from moviepy.editor import VideoFileClip,concatenate_videoclips
from moviepy.editor import concatenate_audioclips, AudioFileClip
from youtube_search import YoutubeSearch
import json
import shutil 
import os.path
from pytube import YouTube
import os
from pydub import AudioSegment
import os
def download_videos_and_convert_into_audio(singer, n):
  search_query = singer + 'music video'

  results = YoutubeSearch(search_query, max_results=n).to_dict()
  for v in results:
   yt= YouTube('https://www.youtube.com' + v['url_suffix'])
   #  print(yt.length)
   video =yt.streams.filter(file_extension='mp4').first()
   destination ="C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Video_files"
   out_file = video.download(output_path=destination)
   basePath, extension = os.path.splitext(out_file)
   video = VideoFileClip(os.path.join(basePath + ".mp4"))
   # video.audio.write_audiofile(os.path.join(basePath + ".mp3"))

def cut_first_y_sec(singer, n, y):
# path to the directory containing the audio files
  directory = "C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Video_files"
  clips=[]
  for filename in os.listdir(directory):
      if filename.endswith(".mp4"):
        file_path = os.path.join(directory, filename)
        clip=VideoFileClip(file_path).subclip(0,y)
        audioclip=clip.audio
        clips.append(audioclip)

  concat = concatenate_audioclips(clips)
#   clips.size  
  
  concat.write_audiofile("C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Audio_files/Merged_Audio_file.mp3")
def funcn(singer,n,y):
   download_videos_and_convert_into_audio(singer, n)
   cut_first_y_sec(singer,n,y)

class contactformemail(forms.Form):
    Email=forms.EmailField(required=True)
    Singer=forms.CharField(required=True)
    Duration=forms.IntegerField(required=True)
    Number_of_videos=forms.IntegerField(required=True)

    # funcn("Singer",Number_of_videos,Duration)


   

# Creating the ZIP file 
# archived = shutil.make_archive("C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Audio_files/Merged_Audio_file.mp3", "C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Zip_files")

# if os.path.exists('E:/Zipped file.zip'):
#    print(archived) 
# else: 
#    print("ZIP file not created")


 

    