from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'title':'Hello'
    }
    return render(request, 'index.html', context)