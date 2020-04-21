from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    if 'user' in request.session:
        return HttpResponseRedirect("/dashboard")

    context={
        'title':'EduLearn'
    }
    return render(request, 'index.html', context)

def login(request):
    if 'user' in request.session:
        return HttpResponseRedirect("/dashboard")

    context={
        'title':'เข้าสู่ระบบ | EduLearn'
    }
    return render(request,'login.html',context)

def register(request):
    if 'user' in request.session:
        return HttpResponseRedirect("/dashboard")

    context={
        'title':'สมัครสมาชิก | EduLearn'
    }
    return render(request,'register.html',context)
