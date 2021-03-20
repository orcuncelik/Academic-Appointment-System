from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.core.mail import send_mail


def teacher(request):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) 
	if "Teacher" == group_name:
		user_name=request.user.get_username()

		appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
		q=request.GET.get("q")
		if q:
			appointment_list=appointment_list.filter(appointment_with__icontains=q)
		else:
			appointment_list = appointment_list

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name
		}
		return render(request, 'teacher.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/') 

def teacher_appointment_list(request):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) 
	if "Teacher" == group_name:
		user_name=request.user.get_username()
		full_name = request.user.get_full_name()
		
		appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
		q=request.GET.get("q")
		if q:
			appointment_list=appointment_list.filter(date__icontains=q)
		else:
			appointment_list = appointment_list

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name, 
			"full_name":full_name,
		    "form":AppointmentForm(),
		}
		form = AppointmentForm(request.POST or None)
		print(request.POST)
		if form.is_valid():
			    saving=form.save(commit=False)
			    saving.user=request.user
			    saving.save()
		return render(request, 'teacher_create_appointment.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/')

  
def appointment_delete(request, id):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) 
	
	u = User.objects.get(username = Appointment.objects.get(id=id).appointment_with)
	teacher = User.objects.get(id = Appointment.objects.get(id=id).user_id)
	appo = Appointment.objects.get(id=id)
	msg = appo.date + ' tarihinde ' + appo.time_start + '-'+ appo.time_end + ' saatleri arasındaki randevunuz iptal edilmiştir. Lütfen öğretmeniniz ' + teacher.first_name + ' ' + teacher.last_name + ' ile iletişime geçiniz. '
	if "Teacher" == group_name:
		single_appointment= Appointment.objects.get(id=id)
		messages.success(request, 'Your profile was updated.')
		#14/1/2021 tarihinde 9.30 - 10.00 saatleri arasındaki randevunuz iptal edilmiştir. Lütfen öğretmeniniz teacherName ile iletişime geçiniz.

		send_mail('RANDEVU İPTALİ', msg , 'yturandevusis@gmail.com',[u.email], fail_silently=False)
		single_appointment.delete()
		return redirect('http://127.0.0.1:8000/teacher/create_appointment/')
	else:
		return redirect('http://127.0.0.1:8000/')

def teacher_appointment_update(request,id):
	group_name=Group.objects.all().filter(user = request.user)
	group_name=str(group_name[0]) 
	if "Teacher" == group_name:
		user_name=request.user.get_username()

		appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
		q=request.GET.get("q") 
		if q:
			appointment_list=appointment_list.filter(date__icontains=q)
		else:
			appointment_list = appointment_list 

		single_appointment = Appointment.objects.get(id=id)
		form = AppointmentForm(request.POST or None, instance=single_appointment)
		if form.is_valid():
			    saving=form.save(commit=False)
			    saving.user=request.user
			    saving.save()
			    messages.success(request, 'Post Created Sucessfully')
			    return redirect('http://127.0.0.1:8000/teacher/create_appointment/')

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name,
		    "form":form,
		}

		return render(request, 'teacher_appointment_update.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/')