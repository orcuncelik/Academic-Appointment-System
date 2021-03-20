from django.contrib.auth.models import User, auth
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import logout
from django import forms
from django.contrib import messages


def group_check(request):
	group_name=Group.objects.all().filter(user = request.user)# 
	group_name=str(group_name[0]) # Stringe çevirme

	if "Student" == group_name:
		return redirect('http://127.0.0.1:8000/student/')
	elif "Teacher" == group_name:
		return redirect('http://127.0.0.1:8000/teacher/')

def logout_view(request):
	logout(request)
	return redirect('http://127.0.0.1:8000/')



def register_teacher(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email1 = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if  password1 == password2:
          user = User.objects.create_user(username = username, email=email1, password=password1, first_name = first_name,last_name=last_name,is_staff = True)
          user.save()
          user.groups.add(1)
          print('user created')
          return redirect('/')
          #RETURN OLARAK HATA METNİ İLE BİRLİKTE ANASAYFAYA YONLENDİR!
        else : 
          messages.error(request,"Şifreler Uyuşmuyor!!") 
          return redirect("register_teacher")    
       
    else:
        return render(request, "register_teacher.html")



def register_student(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email1 = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if  password1 == password2:
          user = User.objects.create_user(username = username, email=email1, password=password1, first_name = first_name,last_name=last_name,is_staff = True)
          user.save()
          user.groups.add(2)
          print('user created')
          return redirect('/')
          #RETURN OLARAK HATA METNİ İLE BİRLİKTE ANASAYFAYA YONLENDİR!
        else : 
          messages.error(request,"Şifreler Uyuşmuyor!!") 
          return redirect("register_student")    

         

    else:
        return render(request, "register_student.html")