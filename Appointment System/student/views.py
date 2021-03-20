from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from teacher.models import Appointment
from teacher.forms import AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def quick_appointment(request):
	group_name=Group.objects.all().filter(user = request.user) 
	group_name=str(group_name[0]) # Stringe çevirme
	if "Student" == group_name:
		user_name=request.user.get_username()
		appointment_list = Appointment.objects.all().order_by("-user")
		q=request.GET.get("q")#Arama
		if q:
			appointment_list=appointment_list.filter(user__first_name__icontains=q)
		else:
			appointment_list = appointment_list

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name,
		}
		return render(request, 'student_quick_appointment.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/')


def student(request):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) #Stringe
	if "Student" == group_name:
		user_name=request.user.get_username()#Kullanıcı Adı Alma
		full_name = request.user.get_full_name()

		appointment_list = Appointment.objects.all().order_by("-id").filter(appointment_with=user_name)
		q=request.GET.get("q")#Arama
		if q:
			appointment_list=appointment_list.filter(user__first_name__icontains=q)
		else:
			appointment_list = appointment_list

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name,    
			"full_name":full_name,
		}
		return render(request, 'student.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/')

def appointment_book(request, id):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) 
	if "Student" == group_name:
		user_name=request.user.get_username()
		single_appointment= Appointment.objects.get(id=id)
		form = single_appointment
		form.appointment_with=user_name
		form.save()
		return redirect('http://127.0.0.1:8000/student/')
	else:
		return redirect('http://127.0.0.1:8000/')




