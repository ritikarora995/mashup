from django.shortcuts import render
from contactformpage.forms import contactformemail
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
import re
import zipfile
from django.conf import settings
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
def zipit(file):
    destination='Mashup.zip'
    zip_file=zipfile.ZipFile(destination,'w')
    zip_file.write(file,compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()
    return destination

def mail(item,em):
    smtp_port = 587           
    smtp_server = "smtp.gmail.com" 
    email_from = "ritikarora995@gmail.com"
    email_to = em
    pswd = "xrjymbvnvlcziymk"
    subject = "Mashup"
    body = f"""
     Mashup Assignment Program 2
    """
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    filename = item
    attachment= open(filename, 'rb') 
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)
    text = msg.as_string()
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()
    print(f"Sending email to: {email_to}...")
    TIE_server.sendmail(email_from, email_to, text)
    print(f"Email sent to: {email_to}")
    print()
    TIE_server.quit()

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
  
  concat.write_audiofile("C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/Merged_Audio_file.mp3")
def funcn(singer,n,y,email):
   folder = 'contactformpage/Video_files'
   for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)  
      if os.path.isfile(file_path) or os.path.islink(file_path): 
        os.unlink(file_path)

   download_videos_and_convert_into_audio(singer, n)
   cut_first_y_sec(singer,n,y)
   file='Merged_Audio_file.mp3'
   mail(zipit(file),email)

def contactsendemail(request):
    if request.method=='GET':
        form=contactformemail()
        return render(request,'contactpage.html',{'form':form})
    else:
        form=contactformemail(request.POST)
        if form.is_valid():
            Email=form.cleaned_data['Email']
            

            Singer=form.cleaned_data['Singer']
            Singer = request.POST.get('Singer')
            Duration = request.POST.get('Duration')
            Number_of_videos=int(request.POST.get('Number_of_videos'))
            funcn(Singer,Number_of_videos,Duration,Email)
   
            
         
            # message.attach_file("C:/Users/raror/OneDrive\Desktop/Semester 6/data science/django_contact_form/contactformpage/contactformpage/Audio_files/Merged_Audio_file.mp3")
            
            # attach_file('contactformpage/Audio_files/Merged_Audio_file.mp3')
            # message="zip"
            # Subject ="Mashup file of "+Singer
            # files = request.FILES.getlist('contactformpage/Audio_files/')

            # # message.attach_file('contactformpage/Audio_files/Merged_Audio_file.mp3')
            # mail = EmailMessage(Subject, message, settings.EMAIL_HOST_USER, [Email])
            # for f in files:
            #     mail.attach(f.name, f.read(), f.content_type)
            # mail.send()
    

            # send_mail(Subject,message,Email,[Email])
    return render(request,'Contactpage.html',{'form':form})