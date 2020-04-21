from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from room import form
from room import models
import json
from django.core import serializers
import hashlib

# Create your views here.
def index(request):
    if 'email' in request.session:
        return HttpResponseRedirect("/dashboard")

    context={
        'title':'EduLearn'
    }
    return render(request, 'index.html', context)

def login(request):
    if 'email' in request.session:
        return HttpResponseRedirect("/dashboard")

    if request.method == 'POST':
        email = request.POST.get('email')
        password=request.POST.get('password')
        password=hashlib.md5(password.encode("utf-8")).hexdigest()

        member=len(models.EdMember.objects.filter(email=email,password=password))
        if member==1:

            member=models.EdMember.objects.get(email=email)
            user_type=models.EdUserType.objects.get(id=member.ed_user_type_id)

            request.session['email']=email
            request.session['type']=user_type.prefix


            from django_user_agents.utils import get_user_agent
            user_agent = get_user_agent(request)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            log=models.EdLog(ip=ip,device=user_agent.device,ed_member_id=member.id)
            log.save()
            

            status=1
        else:
            status=0

        data={
            'status':status
        }

        return JsonResponse(data)

    context={
        'title':'เข้าสู่ระบบ | EduLearn',
    }
    return render(request,'login.html',context)

def logout(request):
    if 'email' in request.session:
        del request.session['email']
    if 'type' in request.session:
        del request.session['type']
    return HttpResponseRedirect("/index")

def register(request):
    if 'email' in request.session:
        return HttpResponseRedirect("/dashboard")

    if request.method == 'POST':
        register=form.RegisterForm(request.POST)
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        edlevel=request.POST.get('edlevel')
        ed_sublevel=request.POST.get('ed_sublevel')
        user_type=request.POST.get('user_type')
        password=request.POST.get('password')
        email=request.POST.get('email')

        password=hashlib.md5(password.encode("utf-8")).hexdigest()

        if len(user_type) == 0 or len(edlevel) == 0 or len(ed_sublevel)== 0:
            status=0
        else:
            member=models.EdMember(email=email,firstname=firstname,lastname=lastname,ed_sub_level_id=ed_sublevel,ed_user_type_id=user_type,password=password)
            member.save()
            status=1
        
        data={
            'status':status
            }
        return JsonResponse(data)
    else:
        register=form.RegisterForm()

    edlevel=models.EdLevel.objects.all()
    user_type=models.EdUserType.objects.all()

    context={
        'title':'สมัครสมาชิก | EduLearn',
        'register':register,
        'edlevel':edlevel,
        'user_type':user_type
    }
    return render(request,'register.html',context)

def dashboard(request):
    if check_email_session(request):
        return HttpResponseRedirect("/login")

    if request.session['type'] == 'STUDENT':

        
        context={
            'title':'หน้าหลักนักเรียน'
        }
        return render(request,'student/dashboard.html',context)
    else:
        context={
            'title':'หน้าหลักครู'
        }
        return render(request,'teacher/dashboard.html',context)


def check_email_session(request):
    if 'email' in request.session:
        return 0
    else:
        return 1

def check_email(request):
    email=request.GET.get('email')
    row=len(models.EdMember.objects.filter(email=email))

    if row >= 1:
        status=0
    else:
        status=1
    data={
        'status':status
    }
    return JsonResponse(data)

def get_ed_sublevel(request):
    edlevel=request.GET.get('edlevel')
    ed_sublevel=models.EdSubLevel.objects.filter(ed_level_id=edlevel).values('id','prefix','title')
    data={'result':list(ed_sublevel)}
    return JsonResponse(data)