from django.shortcuts import render
from ..login_register.models import User

def index(request):
    context = {
        'users': User.objects.all().order_by('-created_on')
    }
    return render(request, 'dashboard/index.html', context)
