from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from room import form
from room import models
import json
from django.core import serializers
import hashlib
from django.core.files.storage import FileSystemStorage

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
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        context={
            'title':'หน้าหลักนักเรียน',
            'member':member
        }
        return render(request,'student/dashboard.html',context)
    else:
        edlevel=models.EdLevel.objects.all()
        user_type=models.EdUserType.objects.all()

        if request.method == 'POST':
            class_name=request.POST.get('class-name')
            class_description=request.POST.get('class-description')
            catagory=request.POST.get('ed_sublevel')

            def generate():
                import random
                chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
                i = 5
                while True:
                    value = "".join(random.choice(chars)
                                    for _ in range(i))
                    row = len(
                        models.EdCourse.objects.filter(uid__iexact=value))

                    if row == 0:
                        return value

                    i = i+1

            uid = generate()

            add_class=models.EdCourse(course_name=class_name,description=class_description,catagory_id=catagory,uid=uid,teacher_id=member.id)
            add_class.save()

            c=models.EdCourse.objects.latest('id')
            enrolment=len(models.EdEnrolment.objects.filter(course_id=c.id))


            data={
                'status':1,
                'latest_course':{'id':c.id,'course_name':c.course_name,'cover_pic':c.cover_pic,'description':c.description,'enrolment':enrolment}
            }
            return JsonResponse(data)
        
        #query course
        course=models.EdCourse.objects.filter(status="ACTIVE").filter(teacher_id=member.id).order_by('-id')

        i=0
        for x in course:
            enrolment=len(models.EdEnrolment.objects.filter(course_id=x.id))
            course[i].enrolment=enrolment
            i=i+1

        context={
            'title':'หน้าหลักครู',
            'member':member,
            'edlevel':edlevel,
            'user_type':user_type,
            'course':course
        }
        return render(request,'teacher/dashboard.html',context)


def classroom(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)
       
    if request.session['type'] == 'STUDENT':
        context={
            'title':'หน้าหลักนักเรียน',
            'member':member
        }
    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        course=models.EdCourse.objects.get(id=classroom_id)

        title=course.course_name
        active_nav = [""]*3
        active_nav[0] = "nav-active"

        context={
            'title':title,
            'member':member,
            'course':course,
            'active_nav':active_nav
        }

        return render(request,'teacher/classroom.html',context)


def check_owner(classroom_id,member_id):
    owner=len(models.EdCourse.objects.filter(id=classroom_id).filter(teacher_id=member_id))
    if owner == 0:
        return 1
    else:
        return 0

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

def update_cover(request):
    classroom_id=request.POST.get('classroom_id')
    files=request.FILES.getlist('cover')
    member_id=request.POST.get('member_id')

    #check session
    if 'email'not in request.session:
        data={
            'status':0
        }
        return JsonResponse(data)

    #check owner
    if check_owner(classroom_id,member_id):
        data={
            'status':0
        }
        return JsonResponse(data)

    if files:

        list = []
        name = []
        file_type = []
        for f in files:
            fs = FileSystemStorage()

            path = "course_id_{0}/cover/{1}"
            path = path.format(
                classroom_id, f.name)
            filename = fs.save(path, f)
            list.append(fs.url(filename))
            name.append(f.name)
            file_type.append(f.content_type)
        
        course=models.EdCourse.objects.get(id=classroom_id)
        course.cover_pic=list[0]
        course.save()

        data={
            'status':1,
            'classroom_id':classroom_id,
            'url':list
        }
        return JsonResponse(data)
