from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from room import form
from room import models
from django.db.models import Q
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

            member=len(models.EdMember.objects.filter(email=email).filter(password=password).filter(status="ACTIVE"))
            if member==1:

                member=models.EdMember.objects.filter(email=email).filter(status="ACTIVE").latest('id')
                user_type=models.EdUserType.objects.get(id=member.user_type_id)

                request.session['email']=email
                request.session['member_id']=member.id
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
                member=models.EdMember.objects.filter(email=email).latest('id')
                if member.status == "PENDING":
                    status=2
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
from django.utils import timezone

def changepass(request,token):

    # if request.method == 'POST':
    #     password=request.POST.get('password')
    #     changepass=len(models.EdChangePass.objects.filter(token=token).filter(status="ACTIVE"))

    #     status=0
    #     if changepass > 0 :
    #         changepass=models.EdChangePass.objects.get(token=token)

    #         dt=changepass.timestamp
    #         b=timezone.now()
    #         dt=b-dt
    #         if dt.days<15:
    #             member=models.EdMember.objects.get(id=changepass.member_id)
    #             password=hashlib.md5(password.encode("utf-8")).hexdigest()
    #             member.password=password
    #             member.save()

    #         changepass.status="DELETE"
    #         changepass.save()
    #         status=1
          

    #     data={
    #         'status':status
    #     }
    #     return JsonResponse(data)
 
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
    if 'member_id' in request.session:
        del request.session['member_id']
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

        row=len(models.EdMember.objects.filter(email=email).filter(status="ACTIVE"))

        if len(user_type) == 0 or len(edlevel) == 0 or len(ed_sublevel)== 0 or row >=1:
            status=0
        else:
            if user_type == '3':
                data={'status':0}
                return JsonResponse(data)
            if user_type == '2':
                member=models.EdMember(email=email,firstname=firstname,lastname=lastname,catagory_id=ed_sublevel,user_type_id=user_type,password=password,status="PENDING")
            else:
                member=models.EdMember(email=email,firstname=firstname,lastname=lastname,catagory_id=ed_sublevel,user_type_id=user_type,password=password)
            member.save()
            status=1
        
        data={
            'status':status,
            }
        return JsonResponse(data)
    else:
        register=form.RegisterForm()

    edlevel=models.EdLevel.objects.all()
    user_type=models.EdUserType.objects.all().exclude(id=3)

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
def get_member(member_id):
    member=models.EdMember.objects.get(id=member_id)
    return member

def dashboard(request):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)
    # member=models.EdMember.objects.get(email=email)

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
    elif request.session['type'] == 'TEACHER':
        edlevel=models.EdLevel.objects.all()
        user_type=models.EdUserType.objects.all()

        if request.method == 'POST':
            class_name=request.POST.get('class-name')
            class_description=request.POST.get('class-description')
            catagory=request.POST.get('ed_sublevel')
            status=request.POST.get('status')
            co_id=request.POST.get('co_id')

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

            if class_name:
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
            elif status:
                co=models.EdCoTeacher.objects.get(id=co_id)
                co.status=status
                co.save()

                if co.status == 'DELETE':
                    status=0
                else:
                    status=1

                data={
                    'status':status,
                    'course_id':co.course_id
                }
                return JsonResponse(data)
        
        #query course
        c=models.EdCourse.objects.filter(status="ACTIVE").filter(teacher_id=member.id).select_related('teacher').order_by('-id')

        co_teacher=models.EdCoTeacher.objects.filter(Q(member_id=member.id),Q(status="ACTIVE")|Q(status="PENDING"))

        course=[]
        for x in c:
            course.append(x)

        for x in co_teacher:
            c=models.EdCourse.objects.get(id=x.course_id)
            c.co=x
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
    elif request.session['type'] == 'ADMIN':
        edlevel=models.EdLevel.objects.all()
        user_type=models.EdUserType.objects.all()

        if request.method == 'POST':
            class_name=request.POST.get('class-name')
            class_description=request.POST.get('class-description')
            catagory=request.POST.get('ed_sublevel')
            status=request.POST.get('status')
            co_id=request.POST.get('co_id')

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

            if class_name:
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
            elif status:
                co=models.EdCoTeacher.objects.get(id=co_id)
                co.status=status
                co.save()

                if co.status == 'DELETE':
                    status=0
                else:
                    status=1

                data={
                    'status':status,
                    'course_id':co.course_id
                }
                return JsonResponse(data)
        
        search_member=models.EdMember.objects.all().select_related('user_type').order_by('-status')
        search_member=search_member.exclude(status="DELETE")

        context={
            'title':'หน้าหลักผู้ดูแลระบบ',
            'member':member,
            'edlevel':edlevel,
            'user_type':user_type,
            'search_member':search_member
        }
        return render(request,'admins/dashboard.html',context)

def overview(request):
    member_id=request.session['member_id']
    member=get_member(member_id)
    if request.session['type'] == 'ADMIN':
        title="ข้อมูลภาพรวม"
        context={
            'title':title,
            'member':member,
        }
        return render(request,'admins/overview.html',context)

def profile(request):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

    member_id=request.session['member_id']
    member=get_member(member_id)
       
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

    elif request.session['type'] == 'TEACHER':
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            description=request.POST.get('course_description')
            email=request.POST.getlist('email[]')
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

            elif email:
                for i in email:
                    row=len(models.EdCoTeacher.objects.filter(member_id=i).filter(course_id=classroom_id).filter(status="ACTIVE"))
                    if row==0:
                        co_teacher=models.EdCoTeacher(course_id=classroom_id,member_id=i)
                        co_teacher.save()

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

    member_id=request.session['member_id']
    member=get_member(member_id)

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


    elif request.session['type'] == 'TEACHER':
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

    member_id=request.session['member_id']
    member=get_member(member_id)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(course_id=classroom_id).filter(status="ACTIVE")

        i=0
        for x in enrolment:
            from django.db.models import Sum
            from collections import OrderedDict
            list={}
            sumscore=0
            for y in task:
                s=len(models.EdTurnedIn.objects.filter(task_id=y.id).filter(status="TURNEDIN").filter(member_id=x.member_id))
                if s==0:
                    score=0
                else:
                    s=models.EdTurnedIn.objects.filter(task_id=y.id).filter(status="TURNEDIN").filter(member_id=x.member_id)
                    score=s[0].score

                list[y.id]=score
                sumscore=sumscore+score

            enrolment[i].score=list
            enrolment[i].sumscore=sumscore
            
            # sum_score=models.EdTurnedIn.objects.filter(member_id=x.member_id).filter(status="TURNEDIN").aggregate(Sum('score'))
            # if sum_score['score__sum']!=0 and sum_score['score__sum']:
            #     enrolment[i].sum_score=sum_score['score__sum']
            # else:
            #     enrolment[i].sum_score=0
            i=i+1

        #sort array
        try:
            enrolment=sorted(enrolment, key= lambda t: t.sumscore, reverse=True)
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
            'enrolment':enrolment,
            'task':task
        }

        return render(request,'student/classroom_score.html',context)

    elif request.session['type'] == 'TEACHER':

        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(course_id=classroom_id).filter(status="ACTIVE")

        i=0
        for x in enrolment:
            from django.db.models import Sum
            from collections import OrderedDict
            list={}
            sumscore=0
            for y in task:
                s=len(models.EdTurnedIn.objects.filter(task_id=y.id).filter(status="TURNEDIN").filter(member_id=x.member_id))
                if s==0:
                    score=0
                else:
                    s=models.EdTurnedIn.objects.filter(task_id=y.id).filter(status="TURNEDIN").filter(member_id=x.member_id)
                    score=s[0].score

                list[y.id]=score
                sumscore=sumscore+score

            enrolment[i].score=list
            enrolment[i].sumscore=sumscore
            
            # sum_score=models.EdTurnedIn.objects.filter(member_id=x.member_id).filter(status="TURNEDIN").aggregate(Sum('score'))
            # if sum_score['score__sum']!=0 and sum_score['score__sum']:
            #     enrolment[i].sum_score=sum_score['score__sum']
            # else:
            #     enrolment[i].sum_score=0
            i=i+1

        #sort array
        try:
            enrolment=sorted(enrolment, key= lambda t: t.sumscore, reverse=True)
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
            'enrolment':enrolment,
            'task':task
        }

        return render(request,'teacher/classroom_score.html',context)
    
def classroom_live(request,classroom_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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
    
    elif request.session['type'] == 'TEACHER':
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

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        sub_task=models.EdSubTask.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('task')

        i=0
        for x in sub_task:
            sub_task_file=models.EdSubTaskFile.objects.filter(sub_task_id=x.id).filter(status="ACTIVE")
            k=0
            for y in sub_task_file:
                if y.file_type.find("image") != -1:
                    sub_task_file[k].type="image"
                elif y.file_type.find("video") != -1:
                    sub_task_file[k].type="video"
                else:
                    sub_task_file[k].type="app"
                k=k+1
            sub_task[i].sub_task_file=sub_task_file
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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")
        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
    
                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1

        context={
            'title':'ปัญหา/ภารกิจ',
            'member':member,
            'course':course,
            'task':task,
            'turnedin':turnedin,
            'is_active':is_active,
            'task_id':task_id,
            'group_bar':group_bar,
            'sub_task':sub_task
        }
        return render(request,'student/main.html',context)

    elif request.session['type'] == 'TEACHER':
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method=='POST':
            file_data=request.FILES.getlist('file')
            file_id=request.POST.getlist('file_id[]')
            link_id=request.POST.getlist('link_id[]')
            steam_div=request.POST.get('steam_div')

            if steam_div or file_id or link_id:

                sub_task=models.EdSubTask(description=steam_div,task_id=task_id,teacher_id=member.id)
                sub_task.save()

                p=models.EdSubTask.objects.latest('id')
                m=models.EdMember.objects.get(id=p.teacher_id)

                if file_id:
                    for i in file_id:
                        f=models.EdSubTaskFile.objects.get(id=i)
                        f.sub_task_id=p.id
                        f.save()
                
                # if link_id:
                #     for i in link_id:
                #         o=models.EdTaskOpengraph.objects.get(id=i)
                #         o.task_id=p.id
                #         o.save()

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

                sub_task_file=models.EdSubTaskFile(file_name=name[0],file_type=file_type[0],file_link=list[0],sub_task_id="")
                sub_task_file.save()

                p=models.EdSubTaskFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('course').order_by('-id')
        
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

        sub_task=models.EdSubTask.objects.filter(task_id=task_id).filter(status="ACTIVE").select_related('teacher').select_related('task')

        i=0
        for x in sub_task:
            sub_task_file=models.EdSubTaskFile.objects.filter(sub_task_id=x.id).filter(status="ACTIVE")
            k=0
            for y in sub_task_file:
                if y.file_type.find("image") != -1:
                    sub_task_file[k].type="image"
                elif y.file_type.find("video") != -1:
                    sub_task_file[k].type="video"
                else:
                    sub_task_file[k].type="app"
                k=k+1
            sub_task[i].sub_task_file=sub_task_file
            i=i+1

        
        #query group
        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        context={
            'title':'ปัญหา/ภารกิจ',
            'member':member,
            'course':course,
            'task':task,
            'is_active':is_active,
            'task_id':task_id,
            'group':group,
            'sub_task':sub_task
        }
        return render(request,'teacher/main.html',context)

def main_score(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")
        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
    
                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1

        context={
            'title':'ให้คะแนน',
            'member':member,
            'course':course,
            'task':task,
            'enrolment':enrolment,
            'group_bar':group_bar
        }
        return render(request,'student/main_score.html',context)
    elif request.session['type'] == 'TEACHER':
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

        #query group
        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        context={
            'title':'ให้คะแนน',
            'member':member,
            'course':course,
            'task':task,
            'enrolment':enrolment,
            'group':group
        }
        return render(request,'teacher/main_score.html',context)

def resource(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")
        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
    
                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1

        context={
            'title':'แหล่งเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'resource':resource,
            'group_bar':group_bar
        }
        return render(request,'student/main_resource.html',context)

    elif request.session['type'] == 'TEACHER':
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

        #query group
        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        context={
            'title':'แหล่งเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'resource':resource,
            'group':group
        }
        return render(request,'teacher/main_resource.html',context)

def scaffolding(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")
        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
    
                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1

        context={
            'title':'ฐานความช่วยเหลือ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'scaff':scaff,
            'scaff_type':scaff_type,
            'group_bar':group_bar
        }
        return render(request,'student/main_scaff.html',context)

    elif request.session['type'] == 'TEACHER':
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

        #query group
        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        context={
            'title':'ฐานความช่วยเหลือ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'scaff':scaff,
            'scaff_type':scaff_type,
            'group':group
        }
        return render(request,'teacher/main_scaff.html',context)

def add_group(request,classroom_id,task_id):
       #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        #query enrolment
        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id).select_related('member')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
                enrolment=enrolment.exclude(member_id=j.member_id)

                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1


        is_active=['']*5
        is_active[3]="active"

        add_col="active"

        context={
            'title':'เพิ่มกลุ่มย่อย',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'enrolment':enrolment,
            'group':group,
            'group_bar':group_bar,
            'is_active':is_active,
            'ad_col':add_col
        }
        return render(request,'student/main_add_collaboration.html',context)


    elif request.session['type'] == 'TEACHER':
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            name=request.POST.getlist('name[]')
            title=request.POST.get('title')

            if title:
                group=models.EdGroup(title=title,task_id=task_id)
                group.save()

                group=models.EdGroup.objects.latest('id')

                for i in name:
                    group_member=models.EdGroupMember(group_id=group.id,member_id=i)
                    group_member.save()
                
                data={
                    'status':1
                }
                return JsonResponse(data)
      

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        #query enrolment
        enrolment=models.EdEnrolment.objects.filter(course_id=classroom_id).select_related('member')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        c=0
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
                enrolment=enrolment.exclude(member_id=j.member_id)
            c=c+1


        is_active=['']*5
        is_active[3]="active"

        add_col="active"

        context={
            'title':'เพิ่มกลุ่มย่อย',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'enrolment':enrolment,
            'group':group,
            'is_active':is_active,
            'ad_col':add_col
        }
        return render(request,'teacher/main_add_collaboration.html',context)

def global_group(request,classroom_id,task_id):
    group_id=None
       #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            # name=request.POST.getlist('steam_div')
            steam_div=request.POST.get('steam_div')
            file_id=request.POST.getlist('file_id[]')
            file_data=request.FILES.getlist('file')
            reply_div=request.POST.get('reply_div')
            colla_id=request.POST.get('colla_id')

            if steam_div or file_id:
                colla=models.EdColla(description=steam_div,member_id=member.id,task_id=task_id,group_id=group_id)
                colla.save()

                colla=models.EdColla.objects.latest('id')

                for i in file_id:
                    f=models.EdCollaFile.objects.get(id=i)
                    f.colla_id=colla.id
                    f.save()

                data={
                    'status':1
                }
                return JsonResponse(data)
            elif reply_div:
                colla_reply=models.EdCollaReply(description=reply_div,member_id=member.id,colla_id=colla_id)
                colla_reply.save()

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
                    path = "course_id_{0}/collaborations/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                colla_file=models.EdCollaFile(file_name=name[0],file_type=file_type[0],file_link=list[0],colla_id="")
                colla_file.save()

                p=models.EdCollaFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:

                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1


        colla=models.EdColla.objects.filter(task_id=task_id).filter(group_id=group_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in colla:
            colla_reply=models.EdCollaReply.objects.filter(colla_id=x.id).filter(status="ACTIVE").select_related('member')
            colla_file=models.EdCollaFile.objects.filter(colla_id=x.id).filter(status="ACTIVE")
            j=0
            for y in colla_file:
                if y.file_type.find("image") != -1:
                    colla_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    colla_file[j].type="video"
                else:
                    colla_file[j].type="app"
                j=j+1

            colla[i].reply=colla_reply
            colla[i].post_file=colla_file
            i=i+1


        is_active=['']*5
        is_active[3]="active"


        context={
            'title':'แลกเปลี่ยนเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'group_bar':group_bar,
            'is_active':is_active,
            'colla':colla
   
        }
        return render(request,'student/main_global_collaboration.html',context)

    elif request.session['type'] == 'TEACHER':
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            # name=request.POST.getlist('steam_div')
            steam_div=request.POST.get('steam_div')
            file_id=request.POST.getlist('file_id[]')
            file_data=request.FILES.getlist('file')
            reply_div=request.POST.get('reply_div')
            colla_id=request.POST.get('colla_id')

            if steam_div or file_id:
                colla=models.EdColla(description=steam_div,member_id=member.id,task_id=task_id,group_id=group_id)
                colla.save()

                colla=models.EdColla.objects.latest('id')

                for i in file_id:
                    f=models.EdCollaFile.objects.get(id=i)
                    f.colla_id=colla.id
                    f.save()

                data={
                    'status':1
                }
                return JsonResponse(data)
            elif reply_div:
                colla_reply=models.EdCollaReply(description=reply_div,member_id=member.id,colla_id=colla_id)
                colla_reply.save()

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
                    path = "course_id_{0}/collaborations/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                colla_file=models.EdCollaFile(file_name=name[0],file_type=file_type[0],file_link=list[0],colla_id="")
                colla_file.save()

                p=models.EdCollaFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)
      

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        c=0
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member
            if i.id == group_id:
                group[c].active="active"
            c=c+1


        colla=models.EdColla.objects.filter(task_id=task_id).filter(group_id=group_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in colla:
            colla_reply=models.EdCollaReply.objects.filter(colla_id=x.id).filter(status="ACTIVE").select_related('member')
            colla_file=models.EdCollaFile.objects.filter(colla_id=x.id).filter(status="ACTIVE")
            j=0
            for y in colla_file:
                if y.file_type.find("image") != -1:
                    colla_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    colla_file[j].type="video"
                else:
                    colla_file[j].type="app"
                j=j+1

            colla[i].reply=colla_reply
            colla[i].post_file=colla_file
            i=i+1


        is_active=['']*5
        is_active[3]="active"


        context={
            'title':'แลกเปลี่ยนเรียนรู้',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'group':group,
            'is_active':is_active,
            'colla':colla
   
        }
        return render(request,'teacher/main_global_collaboration.html',context)

def view_group(request,classroom_id,task_id,group_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

    if request.session['type'] == 'STUDENT':

        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner group
        if check_owner_group(group_id,member.id):
            url="/classroom/{0}/task/{1}/main"
            url=url.format(classroom_id,task_id)
            return HttpResponseRedirect(url)


        if request.method == 'POST':
            # name=request.POST.getlist('steam_div')
            steam_div=request.POST.get('steam_div')
            file_id=request.POST.getlist('file_id[]')
            file_data=request.FILES.getlist('file')
            reply_div=request.POST.get('reply_div')
            colla_id=request.POST.get('colla_id')

            if steam_div or file_id:
                colla=models.EdColla(description=steam_div,member_id=member.id,task_id=task_id,group_id=group_id)
                colla.save()

                colla=models.EdColla.objects.latest('id')

                for i in file_id:
                    f=models.EdCollaFile.objects.get(id=i)
                    f.colla_id=colla.id
                    f.save()

                data={
                    'status':1
                }
                return JsonResponse(data)
            elif reply_div:
                colla_reply=models.EdCollaReply(description=reply_div,member_id=member.id,colla_id=colla_id)
                colla_reply.save()

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
                    path = "course_id_{0}/collaborations/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                colla_file=models.EdCollaFile(file_name=name[0],file_type=file_type[0],file_link=list[0],colla_id="")
                colla_file.save()

                p=models.EdCollaFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)
      

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        view_group=models.EdGroup.objects.get(id=group_id)

        c=0
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member
            if i.id == group_id:
                group[c].active="active"
            c=c+1

        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:

                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1


        colla=models.EdColla.objects.filter(task_id=task_id).filter(group_id=group_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in colla:
            colla_reply=models.EdCollaReply.objects.filter(colla_id=x.id).filter(status="ACTIVE").select_related('member')
            colla_file=models.EdCollaFile.objects.filter(colla_id=x.id).filter(status="ACTIVE")
            j=0
            for y in colla_file:
                if y.file_type.find("image") != -1:
                    colla_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    colla_file[j].type="video"
                else:
                    colla_file[j].type="app"
                j=j+1

            colla[i].reply=colla_reply
            colla[i].post_file=colla_file
            i=i+1


        is_active=['']*5
        is_active[3]="active"



        context={
            'title':view_group.title,
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'group':group,
            'view_group':view_group,
            'is_active':is_active,
            'colla':colla,
            'group_bar':group_bar
   
        }
        return render(request,'student/main_collaboration.html',context)

    elif request.session['type'] == 'TEACHER':
        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")

        if request.method == 'POST':
            # name=request.POST.getlist('steam_div')
            steam_div=request.POST.get('steam_div')
            file_id=request.POST.getlist('file_id[]')
            file_data=request.FILES.getlist('file')
            reply_div=request.POST.get('reply_div')
            colla_id=request.POST.get('colla_id')

            if steam_div or file_id:
                colla=models.EdColla(description=steam_div,member_id=member.id,task_id=task_id,group_id=group_id)
                colla.save()

                colla=models.EdColla.objects.latest('id')

                for i in file_id:
                    f=models.EdCollaFile.objects.get(id=i)
                    f.colla_id=colla.id
                    f.save()

                data={
                    'status':1
                }
                return JsonResponse(data)
            elif reply_div:
                colla_reply=models.EdCollaReply(description=reply_div,member_id=member.id,colla_id=colla_id)
                colla_reply.save()

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
                    path = "course_id_{0}/collaborations/files/{1}/{2}"
                    path = path.format(
                        classroom_id,date,f.name)
                    filename = fs.save(path, f)
                    list.append(fs.url(filename))
                    name.append(f.name)
                    file_type.append(f.content_type)

                colla_file=models.EdCollaFile(file_name=name[0],file_type=file_type[0],file_link=list[0],colla_id="")
                colla_file.save()

                p=models.EdCollaFile.objects.latest('id')

                data={
                    'status':1,
                    'data':{'id':p.id,'file_name':p.file_name,'file_link':p.file_link,'file_type':p.file_type}
                }

                return JsonResponse(data)
      

        #query course
        course=models.EdCourse.objects.get(id=classroom_id)

        #query task
        task=models.EdTask.objects.filter(id=task_id).filter(status="ACTIVE").select_related('teacher')

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        view_group=models.EdGroup.objects.get(id=group_id)

        c=0
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member
            if i.id == group_id:
                group[c].active="active"
            c=c+1


        colla=models.EdColla.objects.filter(task_id=task_id).filter(group_id=group_id).filter(status="ACTIVE").select_related('member').order_by('-id')

        i=0
        for x in colla:
            colla_reply=models.EdCollaReply.objects.filter(colla_id=x.id).filter(status="ACTIVE").select_related('member')
            colla_file=models.EdCollaFile.objects.filter(colla_id=x.id).filter(status="ACTIVE")
            j=0
            for y in colla_file:
                if y.file_type.find("image") != -1:
                    colla_file[j].type="image"
                    
                elif y.file_type.find("video") != -1:
                    colla_file[j].type="video"
                else:
                    colla_file[j].type="app"
                j=j+1

            colla[i].reply=colla_reply
            colla[i].post_file=colla_file
            i=i+1


        is_active=['']*5
        is_active[3]="active"



        context={
            'title':view_group.title,
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'group':group,
            'view_group':view_group,
            'is_active':is_active,
            'colla':colla
   
        }
        return render(request,'teacher/main_collaboration.html',context)

def coaching(request,classroom_id,task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")
        c=0
        group_bar=[]
        for i in group:
            group_member=models.EdGroupMember.objects.filter(group_id=i.id).select_related('member')
            group[c].member=group_member

            for j in group_member:
    
                if j.member_id == member.id:
                    group_bar.append(i)
            c=c+1

        context={
            'title':'ปรึกษาผู้เชียวชาญ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'group_bar':group_bar,
            'coach':coach,
            'co_teacher':co_teacher
        }
        return render(request,'student/main_coach.html',context)

    elif request.session['type'] == 'TEACHER':
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

        group=models.EdGroup.objects.filter(task_id=task_id).filter(status="ACTIVE")

        context={
            'title':'ปรึกษาผู้เชียวชาญ',
            'member':member,
            'course':course,
            'task':task,
            'task_id':task_id,
            'is_active':is_active,
            'coach':coach,
            'group':group,
            'co_teacher':co_teacher
        }
        return render(request,'teacher/main_coach.html',context)

def check_owner(classroom_id,member_id):
    owner=len(models.EdCourse.objects.filter(id=classroom_id).filter(teacher_id=member_id))
    co_teacher=len(models.EdCoTeacher.objects.filter(course_id=classroom_id).filter(member_id=member_id).filter(status="ACTIVE"))
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

def check_owner_colla(colla_id,member_id):
    row=len(models.EdColla.objects.filter(id=colla_id).filter(member_id=member_id))
    if row ==0:
        return 1
    else:
        return 0

def check_owner_group(group_id,member_id):
    row=models.EdGroup.objects.filter(id=group_id).filter(status="ACTIVE")
    if not row:
        return 1
    else:
        row=models.EdGroupMember.objects.filter(member_id=member_id).filter(group_id=group_id)
        if row==0:
            return 1
        else:
            return 0

def delete_live(request,classroom_id,live_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

    member_id=request.session['member_id']
    member=get_member(member_id)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    task=models.EdTask.objects.get(id=task_id)
    task.status="DELETE"
    task.save()

    url="/classroom/{0}/task"
    url=url.format(classroom_id)
    return HttpResponseRedirect(url)

def delete_sub_task(request,classroom_id,task_id,sub_task_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    # check owner task
    if check_owner_task(classroom_id,task_id):
        return HttpResponseRedirect("/dashboard")
    
    sub_task=models.EdSubTask.objects.get(id=sub_task_id)
    sub_task.status="DELETE"
    sub_task.save()

    url="/classroom/{0}/task/{1}/main"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def delete_resource(request,classroom_id,task_id,resource_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

def delete_colla(request,classroom_id,task_id,group_id,colla_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

    if request.session['type'] == 'STUDENT':
        #check enrolment
        if check_enrolment(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check task_enrolment
        if check_enrolment_task(classroom_id,task_id,member.id):
            return HttpResponseRedirect("/dashboard")

        #check owner colla
        if check_owner_colla(colla_id,member.id):
            url=""
            if group_id==0:
                url="/classroom/{0}/task/{1}/global"
            else:
                url="/classroom/{0}/task/{1}/group/{2}"
            url=url.format(classroom_id,task_id,group_id)
            return HttpResponseRedirect(url)

    elif request.session['type'] == 'TEACHER':

        #check owner
        if check_owner(classroom_id,member.id):
            return HttpResponseRedirect("/dashboard")
        
        #check owner task
        if check_owner_task(classroom_id,task_id):
            return HttpResponseRedirect("/dashboard")
        
    colla=models.EdColla.objects.get(id=colla_id)
    colla.status="DELETE"
    colla.save()

    url=""
    if group_id==0:
        url="/classroom/{0}/task/{1}/global"
    else:
        url="/classroom/{0}/task/{1}/group/{2}"
    url=url.format(classroom_id,task_id,group_id)
    return HttpResponseRedirect(url)

def delete_coach(request,classroom_id,task_id,coach_id):
    #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

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

    member_id=request.session['member_id']
    member=get_member(member_id)

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

    member_id=request.session['member_id']
    member=get_member(member_id)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    steam=models.EdPost.objects.get(id=steam_id)
    steam.status="DELETE"
    steam.save()

    url="/classroom/{0}"
    url=url.format(classroom_id)
    return HttpResponseRedirect(url)

def delete_group(request,classroom_id,task_id,group_id):

     #check session
    if 'email'not in request.session:
        return HttpResponseRedirect("/login")

    member_id=request.session['member_id']
    member=get_member(member_id)

    #check owner
    if check_owner(classroom_id,member.id):
        return HttpResponseRedirect("/dashboard")
    
    #check owner task
    if check_owner_task(classroom_id,task_id):
        return HttpResponseRedirect("/dashboard")

    group=models.EdGroup.objects.get(id=group_id)
    group.status="DELETE"
    group.save()

    url="/classroom/{0}/task/{1}/addgroup"
    url=url.format(classroom_id,task_id)
    return HttpResponseRedirect(url)

def check_email(request):
    email=request.GET.get('email')
    row=len(models.EdMember.objects.filter(email=email).filter(status="ACTIVE"))

    if row >= 1:
        status=0
    else:
        status=1
    data={
        'status':status
    }
    return JsonResponse(data)

def get_email(request):
    email=request.GET.get('email')
    course=request.GET.get('course')
    c=models.EdCourse.objects.get(id=course)
    d=models.EdCoTeacher.objects.filter(course_id=course).filter(status="ACTIVE")
    

    member=[]
    if email:
        member=models.EdMember.objects.filter(email__icontains=email).filter(user_type_id=2).exclude(id=c.teacher_id)
        for x in d:
            member=member.exclude(id=x.member_id)
        member=member[:5]

    list=[]
    for x in member:
        list.append({'id':x.id,'email':x.email,'firstname':x.firstname,'lastname':x.lastname})

    status=1
    data={
        'status':status,
        'member':list
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

def update_user(request):
    #check session
    if 'member_id'not in request.session:
        data={
            'status':0
        }
        return JsonResponse(data)

    if request.session['type'] != 'ADMIN':
        data={
            'status':0
        }
        return JsonResponse(data)

    member_id=request.POST.get('member_id')
    status=request.POST.get('status')
    search=request.POST.get('search')

    if member_id:
        member=models.EdMember.objects.get(id=member_id)
        member.status=status
        member.save()

        data={
                'status':1
            }
        return JsonResponse(data)
    elif search or search=="":
        member=models.EdMember.objects.filter(Q(email__icontains=search) | Q(firstname__icontains=search)).select_related('user_type').order_by('-status')
        member=member.exclude(status="DELETE")
        member=member.exclude(user_type=3)
        member=member[:50]
        list=[]
        for i in member:
            list.append({'id':i.id,'email':i.email,'firstname':i.firstname,'lastname':i.lastname,'user_type':i.user_type.title,'status':i.status})
        data={
                'status':1,
                'member':list
            }
        return JsonResponse(data)
    else:
        member=models.EdMember.objects.all().select_related('user_type').order_by('-status')
        member=member.exclude(status="DELETE")
        member=member.exclude(user_type=3)
        member=member[:50]
        list=[]
        for i in member:
            list.append({'id':i.id,'email':i.email,'firstname':i.firstname,'lastname':i.lastname,'user_type':i.user_type.title,'status':i.status})
        data={
                'status':1,
                'member':list
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
    # elif target == 'social':
    #     og = models.EdSocialOpengraph(title='', description='', url='', image='',social_id='')
    #     og.save()

    #     og = models.EdSocialOpengraph.objects.latest('id')
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

from rest_framework.decorators import api_view
from room import serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

@api_view(['GET'])
def api_task_list(request,classroom_id):
    if request.method == 'GET':
        task=models.EdTask.objects.filter(course_id=classroom_id)
        task_serial=serializers.EdTaskSerializer(task,many=True)
        return JsonResponse(task_serial.data, safe=False)

@api_view(['GET', 'POST', 'PUT'])
def api_task_detail(request,classroom_id,task_id):
    try: 
        task=models.EdTask.objects.get(id=task_id)
    except models.EdTask.DoesNotExist: 
        return JsonResponse({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    #check login
    try:
        member_id=request.session['member_id']
    except:
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)  

    #check owner
    if check_owner(classroom_id,member_id):
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)  

    #check owner task
    if check_owner_task(classroom_id,task_id):
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        task_serial=serializers.EdTaskSerializer(task)
        return JsonResponse(task_serial.data)

    elif request.method == 'PUT':

        task_data = JSONParser().parse(request)
        task_serial=serializers.EdTaskSerializer(task,data=task_data)
        if task_serial.is_valid():
            task_serial.save()
            return JsonResponse(task_serial.data)
        return JsonResponse(task_serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT'])
def api_resource_detail(request,classroom_id,task_id,resource_id):
    try: 
        resource=models.EdResource.objects.get(id=resource_id)
    except models.EdResource.DoesNotExist: 
        return JsonResponse({'message': 'The resource does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    #check login
    try:
        member_id=request.session['member_id']
    except:
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)  

    #check owner
    if check_owner(classroom_id,member_id):
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)  

    #check owner task
    if check_owner_task(classroom_id,task_id):
        return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        resource_serial=serializers.EdResourceSerializer(resource)
        return JsonResponse(resource_serial.data)

    elif request.method == "PUT":
        resource_data = JSONParser().parse(request)
        resource_serial=serializers.EdResourceSerializer(resource,data=resource_data)
        if resource_serial.is_valid():
            resource_serial.save()
            return JsonResponse(resource_serial.data)
        return JsonResponse(resource_serial.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models.functions import TruncMonth
from django.db.models import Count
@api_view(['GET', 'POST', 'PUT'])
def api_member_detail(request,command):
    
    if request.method == "GET":
        try:
            admin=request.session['type']
        except:
            return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)

        if admin == 'ADMIN':
            if command == 'register':
                total_member=models.EdMember.objects.annotate(month=TruncMonth('timestamp')).values('month').annotate(c=Count('id')).values('month', 'c')[:12]
                dict={}
                i=0
                for x in total_member:
                    dict.update({i:x})
                    i=i+1
                return JsonResponse(dict)
            elif command=="total":
                row=len(models.EdMember.objects.all())
                return JsonResponse({"total":row})
            elif command == 'member_catagory':
                type_m=models.EdMember.objects.exclude(status="DELETE").values('catagory').annotate(total=Count('id'))
                dict={}
                i=0
                for x in type_m:
                    cat=models.EdSubLevel.objects.get(id=x['catagory'])
                    dict.update({i:{'catagory':cat.title,'total':x['total']}})
                    i=i+1
                return JsonResponse(dict)
            elif command == "member_type":
                type_m=models.EdMember.objects.values('user_type').annotate(total=Count('id'))
                dict={}
                i=0
                for x in type_m:
                    t=models.EdUserType.objects.get(id=x['user_type'])
                    dict.update({i:{'user_type':t.title,'total':x['total']}})
                    i=i+1
                return JsonResponse(dict)
            elif command == "total_room":
                total_room=len(models.EdCourse.objects.all().exclude(status="DELETE"))
                return JsonResponse({'total':total_room})
            elif command == "catagory_room":
                catagory_room=models.EdCourse.objects.exclude(catagory=None).exclude(status="DELETE").values('catagory').annotate(total=Count('id'))
                dict={}
                i=0
                for x in catagory_room:
                    cat=models.EdSubLevel.objects.get(id=x['catagory'])
                    dict.update({i:{'catagory':cat.title,'total':x['total']}})
                    i=i+1
                return JsonResponse(dict)
            else:
                return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)