from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from models import User

def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('dashboard:index'))
    return render(request, 'login_register/index.html')

def signin(request):
    if 'user_id' in request.session:
        return redirect(reverse('login_register:index'))
    return render(request, 'login_register/signin.html')

def signup(request):
    if 'user_id' in request.session:
        return redirect(reverse('login_register:index'))
    return render(request, 'login_register/signup.html')

def login(request):
    res = User.objects.login(request.POST)
    if res['success']:
        request.session['user_id'] = res['user_id']
        request.session['first_name'] = res['first_name']
        request.session['last_name'] = res['last_name']
        request.session['is_admin'] = res['user_level'] == 9
    return redirect(reverse('login_register:signin'))

def register(request):
    if request.method == 'POST':
        u = User.objects.register(request.POST)
    if 'errors' in u:
        return redirect(reverse('login_register:signup'))
    return redirect(reverse('login_register:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('login_register:index'))
