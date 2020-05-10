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

import secrets
from django.core.mail import send_mail
def login(request):
    if 'email' in request.session:
        return HttpResponseRedirect("/dashboard")

    if request.method == 'POST':
        email = request.POST.get('email')
        target = request.POST.get('target')

        if target == "forget":
            member=models.EdMember.objects.get(email=email)
            if member:
                link = secrets.token_urlsafe()

                changepass=models.EdChangePass(member_id=member.id,token=link)
                changepass.save()

                link = "http://"+request.get_host()+"/changepass/"+link
                link = "<p>To change your password please click this link</p><a href="+link+">"+link+"</a>"

                subject = 'Change Your Password'
                message = link
                email_from = 'Edulearn <noreply.edulearn@gmail.com>'
                recipient_list = [email]
                send_mail(subject, link, email_from,
                        recipient_list, html_message=link)


                status=1
            else:
                status=0
            
            data={
                'status':status
            }
            return JsonResponse(data)
                
        else:
            password=request.POST.get('password')
            password=hashlib.md5(password.encode("utf-8")).hexdigest()

            member=len(models.EdMember.objects.filter(email=email,password=password).filter(status="ACTIVE"))
            if member==1:

                member=models.EdMember.objects.get(email=email)
                user_type=models.EdUserType.objects.get(id=member.user_type_id)

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

import datetime 

def changepass(request,token):

    if request.method == 'POST':
        password=request.POST.get('password')
        changepass=len(models.EdChangePass.objects.filter(token=token).filter(status="ACTIVE"))

        status=0
        if changepass > 0 :
            changepass=models.EdChangePass.objects.get(token=token)

            dt=changepass.timestamp
            b=datetime.datetime.now()
            dt=b-dt
            if dt.days<15:
                member=models.EdMember.objects.get(id=changepass.member_id)
                password=hashlib.md5(password.encode("utf-8")).hexdigest()
                member.password=password
                member.save()

            changepass.status="DELETE"
            changepass.save()
            status=1
          

        data={
            'status':status
        }
        return JsonResponse(data)
 
    context={
        'title':'เปลี่ยนรหัสผ่าน',
        'token':token
    }
    return render(request, 'changepass.html', context)


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
            member=models.EdMember(email=email,firstname=firstname,lastname=lastname,catagory_id=ed_sublevel,user_type_id=user_type,password=password)
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

def viewcourse(request):
    if 'email' in request.session:
        return HttpResponseRedirect("/dashboard")

    ed_level=models.EdLevel.objects.all().order_by('-id')

    i=0
    for x in ed_level:
        ed_sublevel=models.EdSubLevel.objects.filter(ed_level_id=x.id)
        ed_level[i].ed_sublevel=ed_sublevel
        j=0
        for y in ed_sublevel:
            course=models.EdCourse.objects.filter(catagory_id=y.id).filter(status='ACTIVE').select_related('teacher').order_by('-id')
            ed_sublevel[j].course=course
            j=j+1
        i=i+1

    course=models.EdCourse.objects.all().select_related('catagory')

    context={
        'title':'ดูคอร์สทั้งหมด | EduLearn',
        'course':course,
        'ed_level':ed_level
    }
    return render(request,'viewcourse.html',context)

def dashboard(request):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':

        if request.method == 'POST':
            uid=request.POST.get('uid')

            row=len(models.EdCourse.objects.filter(uid=uid).filter(status="ACTIVE"))
            if row>0:
                course=models.EdCourse.objects.get(uid=uid)
                row2=len(models.EdEnrolment.objects.filter(member_id=member.id).filter(course_id=course.id))
                if row2>0:
                    data={
                    'status':-1
                    }
                else:
                    enrolment=models.EdEnrolment(member_id=member.id,course_id=course.id)
                    enrolment.save()
                    enrolment=len(models.EdEnrolment.objects.filter(course_id=course.id))


                    c=course
                    
                    data={
                    'status':1,
                    'latest_course':{'id':c.id,'course_name':c.course_name,'cover_pic':c.cover_pic,'description':c.description,'enrolment':enrolment,'firstname':c.teacher.firstname,'lastname':c.teacher.lastname}
                    }
            else:
                data={
                    'status':0
                }
            return JsonResponse(data)
        
        enrolment=models.EdEnrolment.objects.filter(member_id=member.id).order_by("-course_id")
        i=0
        for x in enrolment:
            course=models.EdCourse.objects.filter(id=x.course_id).filter(status="ACTIVE").select_related("teacher").order_by('-id')
            e=len(models.EdEnrolment.objects.filter(course_id=x.course_id))
            enrolment[i].e=e
            enrolment[i].c=course
            i=i+1

        context={
            'title':'หน้าหลักผู้เรียน',
            'member':member,
            'enrolment':enrolment
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
                        models.EdCourse.objects.filter(uid=value))

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
                'latest_course':{'id':c.id,'course_name':c.course_name,'cover_pic':c.cover_pic,'description':c.description,'enrolment':enrolment,'firstname':c.teacher.firstname,'lastname':c.teacher.lastname}
            }
            return JsonResponse(data)
        
        #query course
        c=models.EdCourse.objects.filter(status="ACTIVE").filter(teacher_id=member.id).select_related('teacher').order_by('-id')

        co_teacher=models.EdCoTeacher.objects.filter(member_id=member.id).filter(status="ACTIVE")

        course=[]
        for x in c:
            course.append(x)

        for x in co_teacher:
            c=models.EdCourse.objects.get(id=x.course_id)
            course.append(c)

        course=sorted(course, key= lambda t: t.id, reverse=True)

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

def profile(request):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.method == 'POST':
        file_data=request.FILES.getlist('profile')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        ed_sublevel=request.POST.get('ed_sublevel')

        if firstname:
            member.firstname=firstname
            member.lastname=lastname
            member.catagory_id=ed_sublevel
            member.save()

            data={
                'status':1
            }
            return JsonResponse(data)

        if file_data:
            list = []
            name = []
            file_type = []
            for f in file_data:
                import datetime
                fs = FileSystemStorage()

                date = datetime.date.today()
                path = "member_id_{0}/picture/{1}/{2}"
                path = path.format(
                    member.id,date,f.name)
                filename = fs.save(path, f)
                list.append(fs.url(filename))
                name.append(f.name)
                file_type.append(f.content_type)

            member.picture=list[0]
            member.save()

            data={
                'status':1,
                'data':{'picture':member.picture}
            }

            return JsonResponse(data)

    catagory=models.EdSubLevel.objects.get(id=member.catagory_id)
    super_catagory=models.EdLevel.objects.get(id=catagory.ed_level_id)
    user_type=models.EdUserType.objects.get(id=member.user_type_id)
    member.catagory=catagory
    member.user_type=user_type
    member.super_catagory=super_catagory

    ed_level=models.EdLevel.objects.exclude(id=super_catagory.id)
    ed_sublevel=models.EdSubLevel.objects.exclude(id=catagory.id)
       
    context={
        'title':'โปรไฟล์',
        'member':member,
        'ed_level':ed_level,
        'ed_sublevel':ed_sublevel
    }

    return render(request,'teacher/profile.html',context)

def classroom(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)
       
    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        if request.method == 'POST':
            reply=request.POST.get('reply')
            if reply:
                post_id=request.POST.get('post_id')
                reply=models.EdReply(description=reply,post_id=post_id,member_id=member.id)
                reply.save()

                r=models.EdReply.objects.latest('id')

                data={
                    'status':1
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query co teacher
        co_teacher=models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(status="ACTIVE")

        #query post
        post=models.EdPost.objects.filter(course_id=classroom_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in post:
            reply=models.EdReply.objects.filter(post_id=x.id).filter(status="ACTIVE").select_related('member')
            post_file=models.EdPostFile.objects.filter(post_id=x.id).filter(status="ACTIVE")
            j=0
            for y in post_file:
                if y.file_type.find("image") != -1:
                    post_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    post_file[j].type="video"
                else:
                    post_file[j].type="app"
                j=j+1

            post[i].reply=reply
            post[i].post_file=post_file
            i=i+1


        title=course.course_name
        active_nav = [""]*3
        active_nav[0] = "nav-active"

        context={
            'title':title,
            'member':member,
            'course':course,
            'active_nav':active_nav,
            'post':post,
            'co_teacher':co_teacher
        }
        return render(request,'student/classroom.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            description=request.POST.get('course_description')
            file_id=request.POST.getlist('file_id[]')
            name=request.POST.get('course_name')
            steam_post=request.POST.get('steam_post')
            steam_div=request.POST.get('steam_div')
            reply=request.POST.get('reply')
            file_data=request.FILES.getlist('file')

            if description:
                course=models.EdCourse.objects.get(id=classroom_id)
                course.description=description
                course.save()

                data={
                    'status':1
                }

                return JsonResponse(data)
            elif name:
                course=models.EdCourse.objects.get(id=classroom_id)
                course.course_name=name
                course.save()

                data={
                    'status':1
                }

                return JsonResponse(data)
            elif steam_div or file_id:

                post=models.EdPost(description=steam_div,course_id=classroom_id,member_id=member.id)
                post.save()

                p=models.EdPost.objects.latest('id')
                m=models.EdMember.objects.get(id=p.member_id)

                for i in file_id:
                    f=models.EdPostFile.objects.get(id=i)
                    f.post_id=p.id
                    f.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }

                return JsonResponse(data)
            elif reply:
                post_id=request.POST.get('post_id')
                reply=models.EdReply(description=reply,post_id=post_id,member_id=member.id)
                reply.save()

                r=models.EdReply.objects.latest('id')

                data={
                    'status':1
                }

                return JsonResponse(data)
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    import datetime
                    fs = FileSystemStorage()

                    date = datetime.date.today()
                    path = "course_id_{0}/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                post_file=models.EdPostFile(file_name=name[0],file_type=file_type[0],file_link=list[0],post_id="")
                post_file.save()

                p=models.EdPostFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)



        #query co teacher
        co_teacher=models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(status="ACTIVE")

        #query post
        post=models.EdPost.objects.filter(course_id=classroom_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in post:
            reply=models.EdReply.objects.filter(post_id=x.id).filter(status="ACTIVE").select_related('member')
            post_file=models.EdPostFile.objects.filter(post_id=x.id).filter(status="ACTIVE")
            j=0
            for y in post_file:
                if y.file_type.find("image") != -1:
                    post_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    post_file[j].type="video"
                else:
                    post_file[j].type="app"
                j=j+1

            post[i].reply=reply
            post[i].post_file=post_file
            i=i+1


        title=course.course_name
        active_nav = [""]*3
        active_nav[0] = "nav-active"

        context={
            'title':title,
            'member':member,
            'course':course,
            'active_nav':active_nav,
            'post':post,
            'co_teacher':co_teacher
        }

        return render(request,'teacher/classroom.html',context)

def classroom_task(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(course_id=course.id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        total_task=len(task)

        #query task file
        i=0
        for x in task:
            task_file=models.EdTaskFile.objects.filter(task_id=x.id).filter(status="ACTIVE")
            j=0
            for y in task_file:
                if y.file_type.find("image") != -1:
                    task_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    task_file[j].type="video"
                else:
                    task_file[j].type="app"
                j=j+1
          
            turnedin=models.EdTurnedIn.objects.filter(task_id=x.id).filter(status="TURNEDIN").filter(member_id=member.id)
            task_og=models.EdTaskOpengraph.objects.filter(task_id=x.id)
            total_turnedin=len(turnedin)
            task[i].total_turnedin=total_turnedin
            task[i].task_file=task_file
            task[i].og=task_og

            try:
                percent=total_turnedin/1*100
                percent=round(percent,2)
            except ZeroDivisionError:
                percent=0
            
            task[i].percent=percent

            i=i+1

        title=course.course_name
        active_nav = [""]*3
        active_nav[1] = "nav-active"

        context={
            'title':title,
            'member':member,
            'course':course,
            'active_nav':active_nav,
            'task':task,
            'total_task':total_task
        }

        return render(request,'student/classroom_task.html',context)

        context={
            'title':'หน้าหลักผู้เรียน',
            'member':member
        }


    else:
        #check enrolment
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        if request.method == 'POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')

            if steam_div or file_id or link_id:

                post=models.EdTask(description=steam_div,course_id=classroom_id,teacher_id=member.id)
                post.save()

                p=models.EdTask.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdTaskFile.objects.get(id=i)
                        f.task_id=p.id
                        f.save()
                
                if link_id:
                    for i in link_id:
                        o=models.EdTaskOpengraph.objects.get(id=i)
                        o.task_id=p.id
                        o.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    import datetime
                    fs = FileSystemStorage()

                    date = datetime.date.today()
                    path = "course_id_{0}/task/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                post_file=models.EdTaskFile(file_name=name[0],file_type=file_type[0],file_link=list[0],task_id="")
                post_file.save()

                p=models.EdTaskFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)
        
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(course_id=course.id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        total_task=len(task)

        total_member=len(models.EdEnrolment.objects.filter(course_id=classroom_id))

        #query task file
        i=0
        for x in task:
            task_file=models.EdTaskFile.objects.filter(task_id=x.id).filter(status="ACTIVE")
            j=0
            for y in task_file:
                if y.file_type.find("image") != -1:
                    task_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    task_file[j].type="video"
                else:
                    task_file[j].type="app"
                j=j+1
          
            turnedin=models.EdTurnedIn.objects.filter(task_id=x.id).filter(status="TURNEDIN")
            task_og=models.EdTaskOpengraph.objects.filter(task_id=x.id)
            total_turnedin=len(turnedin)
            task[i].total_turnedin=total_turnedin
            task[i].task_file=task_file
            task[i].og=task_og

            try:
                percent=total_turnedin/total_member*100
                percent=round(percent,2)
            except ZeroDivisionError:
                percent=0
            
            task[i].percent=percent

            i=i+1

        title=course.course_name
        active_nav = [""]*3
        active_nav[1] = "nav-active"

        context={
            'title':title,
            'member':member,
            'course':course,
            'active_nav':active_nav,
            'task':task,
            'total_task':total_task,
            'total_member':total_member
        }

        return render(request,'teacher/classroom_task.html',context)

def classroom_score(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        i=0
        for x in enrolment:
            from django.db.models import Sum
            from collections import OrderedDict
            sum_score=models.EdTurnedIn.objects.filter(member_id=x.member_id).filter(status="TURNEDIN").aggregate(Sum('score'))
            enrolment[i].sum_score=sum_score['score__sum']
            i=i+1

        #sort array
        try:
            enrolment=sorted(enrolment, key= lambda t: t.sum_score, reverse=True)
        except:
            enrolment=enrolment

        title=course.course_name
        active_nav = [""]*3
        active_nav[2] = "nav-active"

        context={
            'title':title,
            'member':member,
            'active_nav':active_nav,
            'course':course,
            'enrolment':enrolment
        }

        return render(request,'student/classroom_score.html',context)

    else:

        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        i=0
        for x in enrolment:
            from django.db.models import Sum
            from collections import OrderedDict
            sum_score=models.EdTurnedIn.objects.filter(member_id=x.member_id).filter(status="TURNEDIN").aggregate(Sum('score'))
            enrolment[i].sum_score=sum_score['score__sum']
            i=i+1

        #sort array
        try:
            enrolment=sorted(enrolment, key= lambda t: t.sum_score, reverse=True)
        except:
            enrolment=enrolment

        title=course.course_name
        active_nav = [""]*3
        active_nav[2] = "nav-active"

        context={
            'title':title,
            'member':member,
            'active_nav':active_nav,
            'course':course,
            'enrolment':enrolment
        }

        return render(request,'teacher/classroom_score.html',context)
    
def classroom_live(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query live
        live=models.EdLive.objects.filter(course_id=classroom_id).filter(status="ACTIVE")
       
        title=course.course_name
        active_nav = [""]*4
        active_nav[3] = "nav-active"

        context={
            'title':title,
            'member':member,
            'active_nav':active_nav,
            'course':course,
            'live':live
        }

        return render(request,'student/classroom_live.html',context)
    
    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            live_id=request.POST.get('id')
            platform=request.POST.get('platform')
            password=request.POST.get('password')

            if live_id:
                live=models.EdLive(teacher_id=member.id,course_id=classroom_id,url=live_id,password=password,platform=platform)
                live.save()

                data={
                    'status':1
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query live
        live=models.EdLive.objects.filter(course_id=classroom_id).filter(status="ACTIVE")
       
        title=course.course_name
        active_nav = [""]*4
        active_nav[3] = "nav-active"

        context={
            'title':title,
            'member':member,
            'active_nav':active_nav,
            'course':course,
            'live':live
        }

        return render(request,'teacher/classroom_live.html',context)

def main(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')

            if steam_div or file_id or link_id:

                t=models.EdTurnedIn.objects.filter(task_id=task_id).filter(member_id=member.id).filter(status="TURNEDIN")
                for i in t:
                    i.status="DELETE"
                    i.save()

                turnedin=models.EdTurnedIn(description=steam_div,task_id=task_id,member_id=member.id)
                turnedin.save()

                p=models.EdTurnedIn.objects.latest('id')
                m=models.EdMember.objects.get(id=p.member_id)

                if file_id:
                    for i in file_id:
                        f=models.EdTurnedinFile.objects.get(id=i)
                        f.turnedin_id=p.id
                        f.save()
                
                if link_id:
                    for i in link_id:
                        o=models.EdTurnedinOpengraph.objects.get(id=i)
                        o.turnedin_id=p.id
                        o.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    import datetime
                    fs = FileSystemStorage()

                    date = datetime.date.today()
                    path = "course_id_{0}/turnedin/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                turnedin_file=models.EdTurnedinFile(file_name=name[0],file_type=file_type[0],file_link=list[0],turnedin_id="")
                turnedin_file.save()

                p=models.EdTurnedinFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('course')
        
        is_active=['']*5
        is_active[0]="active"

        #query task file
        i=0
        for x in task:
            task_file=models.EdTaskFile.objects.filter(task_id=x.id).filter(status="ACTIVE")
            k=0
            for y in task_file:
                if y.file_type.find("image") != -1:
                    task_file[k].type="image"
                elif y.file_type.find("video") != -1:
                    task_file[k].type="video"
                else:
                    task_file[k].type="app"
                k=k+1
            turnedin=models.EdTurnedIn.objects.filter(task_id=x.id).filter(status="TURNEDIN").filter(member_id=member.id)
            task_og=models.EdTaskOpengraph.objects.filter(task_id=x.id)
            total_turnedin=len(turnedin)
            task[i].total_turnedin=total_turnedin
            task[i].task_file=task_file
            task[i].og=task_og

            try:
                percent=total_turnedin/1*100
                percent=round(percent,2)
            except ZeroDivisionError:
                percent=0
            
            task[i].percent=percent

            i=i+1

        #query turnedin
        turnedin=models.EdTurnedIn.objects.filter(status="TURNEDIN").filter(task_id=task_id).filter(member_id=member.id)
        #query turnedin file
        i=0
        for x in turnedin:
            turnedin_file=models.EdTurnedinFile.objects.filter(turnedin_id=x.id).filter(status="ACTIVE")
            k=0
            for y in turnedin_file:
                if y.file_type.find("image") != -1:
                    turnedin_file[k].type="image"
                elif y.file_type.find("video") != -1:
                    turnedin_file[k].type="video"
                else:
                    turnedin_file[k].type="app"
                k=k+1
            turnedin_og=models.EdTurnedinOpengraph.objects.filter(turnedin_id=x.id)
            turnedin[i].turnedin_file=turnedin_file
            turnedin[i].og=turnedin_og
            i=i+1

        context={
            'title':'ภารกิจ',
            'member':member,
            'course':course,
            'task':task,
            'turnedin':turnedin,
            'is_active':is_active,
            'task_id':task_id
        }
        return render(request,'student/main.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('course')
        
        is_active=['']*5
        is_active[0]="active"

        #query task file
        i=0
        for x in task:
            total_member=len(models.EdEnrolment.objects.filter(course_id=x.course_id))
            task_file=models.EdTaskFile.objects.filter(task_id=x.id).filter(status="ACTIVE")
            k=0
            for y in task_file:
                if y.file_type.find("image") != -1:
                    task_file[k].type="image"
                elif y.file_type.find("video") != -1:
                    task_file[k].type="video"
                else:
                    task_file[k].type="app"
                k=k+1
            turnedin=models.EdTurnedIn.objects.filter(task_id=x.id).filter(status="TURNEDIN")
            task_og=models.EdTaskOpengraph.objects.filter(task_id=x.id)
            total_turnedin=len(turnedin)
            task[i].total_turnedin=total_turnedin
            task[i].task_file=task_file
            task[i].og=task_og
            task[i].total_member=total_member

            try:
                percent=total_turnedin/total_member*100
                percent=round(percent,2)
            except ZeroDivisionError:
                percent=0
            
            task[i].percent=percent

            i=i+1

        context={
            'title':'ภารกิจ',
            'member':member,
            'course':course,
            'task':task,
            'is_active':is_active,
            'task_id':task_id
        }
        return render(request,'teacher/main.html',context)

def main_score(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('course')

        #query enrolment
        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        #query turnedin
        i=0
        for e in enrolment:
            turnedin=models.EdTurnedIn.objects.filter(member_id=e.member_id).filter(status="TURNEDIN").filter(task_id=task_id)
            if len(turnedin)>0:
                turnedin_status='turnedin'
            else:
                turnedin_status='wait'
            j=0
            for f in turnedin:
                turnedin_file=models.EdTurnedinFile.objects.filter(turnedin_id=f.id).filter(status="ACTIVE")
                k=0
                for y in turnedin_file:
                    if y.file_type.find("image") != -1:
                        turnedin_file[k].type="image"
                    elif y.file_type.find("video") != -1:
                        turnedin_file[k].type="video"
                    else:
                        turnedin_file[k].type="app"
                    k=k+1

                turnedin_og=models.EdTurnedinOpengraph.objects.filter(turnedin_id=f.id)
                turnedin[j].turnedin_file=turnedin_file
                turnedin[j].og=turnedin_og
                j=j+1
            enrolment[i].turnedin=turnedin
            enrolment[i].turnedin_status=turnedin_status
            i=i+1

        context={
            'title':'ให้คะแนน',
            'member':member,
            'course':course,
            'task':task,
            'enrolment':enrolment
        }
        return render(request,'student/main_score.html',context)
    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            turnedin_id=request.POST.get('turnedin_id')
            score=request.POST.get('score')

            t=models.EdTurnedIn.objects.get(id=turnedin_id)
            t.score=score
            t.save()

            data={
                'status':1
            }
            return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('course')

        #query enrolment
        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        #query turnedin
        i=0
        for e in enrolment:
            turnedin=models.EdTurnedIn.objects.filter(member_id=e.member_id).filter(status="TURNEDIN")
            if len(turnedin)>0:
                turnedin_status='turnedin'
            else:
                turnedin_status='wait'
            j=0
            for f in turnedin:
                turnedin_file=models.EdTurnedinFile.objects.filter(turnedin_id=f.id).filter(status="ACTIVE")
                k=0
                for y in turnedin_file:
                    if y.file_type.find("image") != -1:
                        turnedin_file[k].type="image"
                    elif y.file_type.find("video") != -1:
                        turnedin_file[k].type="video"
                    else:
                        turnedin_file[k].type="app"
                    k=k+1

                turnedin_og=models.EdTurnedinOpengraph.objects.filter(turnedin_id=f.id)
                turnedin[j].turnedin_file=turnedin_file
                turnedin[j].og=turnedin_og
                j=j+1
            enrolment[i].turnedin=turnedin
            enrolment[i].turnedin_status=turnedin_status
            i=i+1

        context={
            'title':'ให้คะแนน',
            'member':member,
            'course':course,
            'task':task,
            'enrolment':enrolment
        }
        return render(request,'teacher/main_score.html',context)

def resource(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query resource
        resource=models.EdResource.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in resource:
            resource_file=models.EdResourceFile.objects.filter(resource=x.id).filter(status="ACTIVE")
            j=0
            for y in resource_file:
                if y.file_type.find("image") != -1:
                    resource_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    resource_file[j].type="video"
                else:
                    resource_file[j].type="app"
                j=j+1

            resource_og=models.EdResourceOpengraph.objects.filter(resource_id=x.id)
            resource[i].resource_file=resource_file
            resource[i].og=resource_og  
    
            i=i+1          

        is_active=['']*5
        is_active[1]="active"

        context={
            'title':'แหล่งเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'resource':resource
        }
        return render(request,'student/main_resource.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')

            if steam_div or file_id or link_id:

                post=models.EdResource(description=steam_div,task_id=task_id,teacher_id=member.id)
                post.save()

                p=models.EdResource.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdResourceFile.objects.get(id=i)
                        f.resource_id=p.id
                        f.save()
                
                if link_id:
                    for i in link_id:
                        o=models.EdResourceOpengraph.objects.get(id=i)
                        o.resource_id=p.id
                        o.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    import datetime
                    fs = FileSystemStorage()

                    date = datetime.date.today()
                    path = "course_id_{0}/resource/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                resource_file=models.EdResourceFile(file_name=name[0],file_type=file_type[0],file_link=list[0],resource_id="")
                resource_file.save()

                p=models.EdResourceFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query resource
        resource=models.EdResource.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in resource:
            resource_file=models.EdResourceFile.objects.filter(resource=x.id).filter(status="ACTIVE")
            j=0
            for y in resource_file:
                if y.file_type.find("image") != -1:
                    resource_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    resource_file[j].type="video"
                else:
                    resource_file[j].type="app"
                j=j+1

            resource_og=models.EdResourceOpengraph.objects.filter(resource_id=x.id)
            resource[i].resource_file=resource_file
            resource[i].og=resource_og  
    
            i=i+1          

        is_active=['']*5
        is_active[1]="active"

        context={
            'title':'แหล่งเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'resource':resource
        }
        return render(request,'teacher/main_resource.html',context)

def scaffolding(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query scaff_type
        scaff_type=models.EdScaffoldingType.objects.all()

        #query scaffolding
        scaff=models.EdScaffolding.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in scaff:
            scaff_file=models.EdScaffoldingFile.objects.filter(scaffolding_id=x.id).filter(status="ACTIVE")
            j=0
            for y in scaff_file:
                if y.file_type.find("image") != -1:
                    scaff_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    scaff_file[j].type="video"
                else:
                    scaff_file[j].type="app"
                j=j+1

            scaff[i].scaff_file=scaff_file
            i=i+1          

        is_active=['']*5
        is_active[2]="active"

        context={
            'title':'ฐานความช่วยเหลือ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'scaff':scaff,
            'scaff_type':scaff_type
        }
        return render(request,'student/main_scaff.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')
            scaff_type=request.POST.get('scaff_type')

            if steam_div or file_id or link_id:
                s=models.EdScaffolding.objects.filter(task_id=task_id).filter(scaff_type_id=scaff_type)
                for i in s:
                    i.status="DELETE"
                    i.save()

                post=models.EdScaffolding(description=steam_div,task_id=task_id,teacher_id=member.id,scaff_type_id=scaff_type)
                post.save()

                p=models.EdScaffolding.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdScaffoldingFile.objects.get(id=i)
                        f.scaffolding_id=p.id
                        f.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    if f.content_type.find("image") != -1:
                        import datetime
                        fs = FileSystemStorage()

                        date = datetime.date.today()
                        path = "course_id_{0}/scaffolding/files/{1}/{2}"
                        path = path.format(
                            classroom_id,date,f.name)
                        filename = fs.save(path, f)
                        list.append(fs.url(filename))
                        name.append(f.name)
                        file_type.append(f.content_type)

                scaff_file=models.EdScaffoldingFile(file_name=name[0],file_type=file_type[0],file_link=list[0],scaffolding_id="")
                scaff_file.save()

                p=models.EdScaffoldingFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query scaff_type
        scaff_type=models.EdScaffoldingType.objects.all()

        #query scaffolding
        scaff=models.EdScaffolding.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in scaff:
            scaff_file=models.EdScaffoldingFile.objects.filter(scaffolding_id=x.id).filter(status="ACTIVE")
            j=0
            for y in scaff_file:
                if y.file_type.find("image") != -1:
                    scaff_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    scaff_file[j].type="video"
                else:
                    scaff_file[j].type="app"
                j=j+1

            scaff[i].scaff_file=scaff_file
            i=i+1          

        is_active=['']*5
        is_active[2]="active"

        context={
            'title':'ฐานความช่วยเหลือ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'scaff':scaff,
            'scaff_type':scaff_type
        }
        return render(request,'teacher/main_scaff.html',context)

def social(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query resource
        social=models.EdSocial.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in social:
            social_file=models.EdSocialFile.objects.filter(social_id=x.id).filter(status="ACTIVE")
            j=0
            for y in social_file:
                if y.file_type.find("image") != -1:
                    social_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    social_file[j].type="video"
                else:
                    social_file[j].type="app"
                j=j+1

            social_og=models.EdSocialOpengraph.objects.filter(social_id=x.id)
            social[i].social_file=social_file
            social[i].og=social_og  
    
            i=i+1          

        is_active=['']*5
        is_active[3]="active"

        context={
            'title':'ชุมชนการเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'social':social
        }
        return render(request,'student/main_social.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')

            if steam_div or file_id or link_id:

                post=models.EdSocial(description=steam_div,task_id=task_id,teacher_id=member.id)
                post.save()

                p=models.EdSocial.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdSocialFile.objects.get(id=i)
                        f.social_id=p.id
                        f.save()
                
                if link_id:
                    for i in link_id:
                        o=models.EdSocialOpengraph.objects.get(id=i)
                        o.social_id=p.id
                        o.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'description':p.description,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    import datetime
                    fs = FileSystemStorage()

                    date = datetime.date.today()
                    path = "course_id_{0}/social/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                social_file=models.EdSocialFile(file_name=name[0],file_type=file_type[0],file_link=list[0],social_id="")
                social_file.save()

                p=models.EdSocialFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query resource
        social=models.EdSocial.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in social:
            social_file=models.EdSocialFile.objects.filter(social_id=x.id).filter(status="ACTIVE")
            j=0
            for y in social_file:
                if y.file_type.find("image") != -1:
                    social_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    social_file[j].type="video"
                else:
                    social_file[j].type="app"
                j=j+1

            social_og=models.EdSocialOpengraph.objects.filter(social_id=x.id)
            social[i].social_file=social_file
            social[i].og=social_og  
    
            i=i+1          

        is_active=['']*5
        is_active[3]="active"

        context={
            'title':'ชุมชนการเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'social':social
        }
        return render(request,'teacher/main_social.html',context)

def coaching(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query co teacher
        co_teacher=models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query coach
        coach=models.EdCoach.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in coach:
            coach_file=models.EdCoachFile.objects.filter(coach_id=x.id).filter(status="ACTIVE")
            j=0
            for y in coach_file:
                if y.file_type.find("image") != -1:
                    coach_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    coach_file[j].type="video"
                else:
                    coach_file[j].type="app"
                j=j+1

            coach[i].coach_file=coach_file
    
            i=i+1          

        is_active=['']*5
        is_active[4]="active"

        context={
            'title':'ปรึกษาผู้เชียวชาญ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'coach':coach,
            'co_teacher':co_teacher
        }
        return render(request,'student/main_coach.html',context)

    else:
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            file_data=request.FILES.getlist('coach')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            name=request.POST.get('name')
            email=request.POST.get('email')

            if name or email or file_id:

                post=models.EdCoach(name=name,email=email,task_id=task_id,teacher_id=member.id)
                post.save()

                p=models.EdCoach.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdCoachFile.objects.get(id=i)
                        f.coach_id=p.id
                        f.save()

                data={
                    'status':1,
                    'data':{'id':p.id,'name':p.name,'email':p.email,'timestamp':p.timestamp,'firstname':m.firstname,'lastname':m.lastname,'picture':m.picture}
                }
                return JsonResponse(data)
            
            if file_data:

                list = []
                name = []
                file_type = []
                for f in file_data:
                    if f.content_type.find('image') !=- 1:
                        import datetime
                        fs = FileSystemStorage()

                        date = datetime.date.today()
                        path = "course_id_{0}/coach/files/{1}/{2}"
                        path = path.format(
                            classroom_id,date,f.name)
                        filename = fs.save(path, f)
                        list.append(fs.url(filename))
                        name.append(f.name)
                        file_type.append(f.content_type)

                coach_file=models.EdCoachFile(file_name=name[0],file_type=file_type[0],file_link=list[0],coach_id="")
                coach_file.save()

                p=models.EdCoachFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query co teacher
        co_teacher=models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query coach
        coach=models.EdCoach.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').order_by('-id')
        i=0
        for x in coach:
            coach_file=models.EdCoachFile.objects.filter(coach_id=x.id).filter(status="ACTIVE")
            j=0
            for y in coach_file:
                if y.file_type.find("image") != -1:
                    coach_file[j].type="image"
                elif y.file_type.find("video") != -1:
                    coach_file[j].type="video"
                else:
                    coach_file[j].type="app"
                j=j+1

            coach[i].coach_file=coach_file
    
            i=i+1          

        is_active=['']*5
        is_active[4]="active"

        context={
            'title':'ปรึกษาผู้เชียวชาญ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'coach':coach,
            'co_teacher':co_teacher
        }
        return render(request,'teacher/main_coach.html',context)

def check_owner(classroom_id,member_id):
    owner=len(models.EdCourse.objects.filter(id=classroom_id).filter(teacher_id=member_id))
    co_teacher=len(models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(member_id=member_id))
    if owner == 0 and co_teacher == 0:
        return 1
    else:
        return 0

def check_owner_task(classroom_id,task_id):
    row = len(models.EdTask.objects.filter(course_id=classroom_id).filter(id=task_id).filter(status="active"))
    if row == 0:
        return 1
    else:
        return 0

def check_enrolment(course_id,member_id):
    row1=len(models.EdEnrolment.objects.filter(course_id=course_id).filter(member_id=member_id))
    if row1 == 0:
        return 1
    else:
        return 0

def check_enrolment_task(course_id,task_id,member_id):
    row2=len(models.EdTask.objects.filter(course_id=course_id).filter(id=task_id).filter(status="ACTIVE"))
    if row2 == 0:
         return 1
    else:
        return 0

def delete_live(request,classroom_id,live_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    live=models.EdLive.objects.get(id=live_id)
    live.status="DELETE"
    live.save()

    url="/classroom/{0}/live"
    url=url.format(classroom_id)
    return HttpResponseRedirect(url)

def delete_task(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    task=models.EdTask.objects.get(id=task_id)
    task.status="DELETE"
    task.save()

    url="/classroom/{0}/task"
    url=url.format(classroom_id)
    return HttpResponseRedirect(url)

def delete_resource(request,classroom_id,task_id,resource_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    #check owner task
    if check_owner_task(classroom_id,task_id):
        return HttpResponseRedirect("/dashboard")
    
    resource=models.EdResource.objects.get(id=resource_id)
    resource.status="DELETE"
    resource.save()

    url="/classroom/{0}/task/{1}/resource"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def delete_social(request,classroom_id,task_id,social_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    #check owner task
    if check_owner_task(classroom_id,task_id):
        return HttpResponseRedirect("/dashboard")
    
    resource=models.EdSocial.objects.get(id=social_id)
    resource.status="DELETE"
    resource.save()

    url="/classroom/{0}/task/{1}/social"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def delete_coach(request,classroom_id,task_id,coach_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    #check owner task
    if check_owner_task(classroom_id,task_id):
        return HttpResponseRedirect("/dashboard")
    
    coach=models.EdCoach.objects.get(id=coach_id)
    coach.status="DELETE"
    coach.save()

    url="/classroom/{0}/task/{1}/coach"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def delete_turnin(request,classroom_id,task_id,turnedin_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check enrolment
    if check_enrolment(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")

    #check task_enrolment
    if check_enrolment_task(classroom_id,task_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    t=models.EdTurnedIn.objects.get(id=turnedin_id)
    t.status="DELETE"
    t.save()

    url="/classroom/{0}/task/{1}/main"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def delete_steam(request,classroom_id,steam_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    email=request.session['email']
    member=models.EdMember.objects.get(email=email)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    steam=models.EdPost.objects.get(id=steam_id)
    steam.status="DELETE"
    steam.save()

    url="/classroom/{0}"
    url=url.format(classroom_id)
    return HttpResponseRedirect(url)


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

import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

def fetch_og(request):
    
    url_req=request.GET.get('url')
    target=request.GET.get('target')

    page = urllib.request.urlopen(url_req).read()
    html = BeautifulSoup(page)
    title = html.find("meta",  property="og:title")
    description = html.find("meta",  property="og:description")
    url = html.find("meta",  property="og:url")
    image = html.find("meta",  property="og:image")

    og=[]

    if target == 'task':
        og = models.EdTaskOpengraph(title='', description='', url='', image='',task_id="")
        og.save()

        og = models.EdTaskOpengraph.objects.latest('id')
    elif target == 'resource':
        og = models.EdResourceOpengraph(title='', description='', url='', image='',resource_id='')
        og.save()

        og = models.EdResourceOpengraph.objects.latest('id')
    elif target == 'social':
        og = models.EdSocialOpengraph(title='', description='', url='', image='',social_id='')
        og.save()

        og = models.EdSocialOpengraph.objects.latest('id')
    elif target == 'turnedin':
        og = models.EdTurnedinOpengraph(title='', description='', url='', image='',turnedin_id='')
        og.save()

        og = models.EdTurnedinOpengraph.objects.latest('id')

    if title is None:
        title=html.find("title")
        og.title = title
    else:
        og.title = title['content']
        og.save()
    if description is None:
        og.description = ""
    else:
        og.description = description['content']
        og.save()
    if image is None:
        og.image = ""
    else:
        if 'http' not in image['content']:
            if url_req.endswith('/'):
                url_req=url_req[0:-1]
            image['content']=url_req+image['content']
        og.image = image['content']
        og.save()
    if url is None:
        og.url = url_req
    else:
        og.url = url['content']
        og.save()

    data={
        'status':1,
        'og':{'id':og.id,'title':og.title,'image':og.image,'url':og.url,'description':og.description}
    }
    return JsonResponse(data)