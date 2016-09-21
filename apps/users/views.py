from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from ..login_register.models import User

def index(request):
    return redirect(reverse('dashboard:index'))

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'messages': []
    }
    return render(request, 'users/show_user.html')

def new_user_admin(request):
    if request.session['is_admin']:
        return render(request, 'users/new_user.html')
    return redirect(reverse('dashboard:index'))

def edit_user_admin(request, user_id):
    if request.session['is_admin']:
        context = {
            'user': User.objects.get(id=user_id)
        }
        return render(request, 'users/edit_user.html', context)
    return redirect(reverse('users:edit_user'))

def edit_user(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/edit_user.html', context)

def destroy_user_admin(request, user_id):
    if request.method == 'POST':
        User.objects.delete_user(request.session['user_id'], user_id, request.session['is_admin'])
    return redirect(reverse('dashboard:index'))

def create_user_admin(request):
    if request.method == 'POST':
        User.objects.create_user(request.POST, request.session['is_admin'])
    return redirect(reverse('dashboard:index'))

def update_user(request, user_id):
    if request.method == 'POST':
        res = User.objects.update_user(request.session['user_id'], user_id, request.POST, request.session['is_admin'])
        if not res['updated']:
            return redirect(reverse('users:edit_user'))
    return redirect(reverse('dashboard:index'))
