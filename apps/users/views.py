from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from ..login_register.models import User
from models import Message,Comment

def index(request):
    return redirect(reverse('dashboard:index'))

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'messages': Message.objects.filter(user_to=user_id).order_by('-created_on')
    }

    return render(request, 'users/show_user.html', context)

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

def post_comment(request, message_id):
    user = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=message_id)
    comment = Comment.objects.create(message=message,user=user,comment=request.POST['comment'])
    comment.save()
    return redirect(reverse('users:show_user', kwargs={'user_id': message.user_to.id}))

def post_message(request, user_id):
    user_to = User.objects.get(id=user_id)
    user_from = User.objects.get(id=request.session['user_id'])
    message = Message.objects.create(user_to=user_to, user_from=user_from, message=request.POST['message'])
    message.save()
    return redirect(reverse('users:show_user', kwargs={'user_id': user_id}))
