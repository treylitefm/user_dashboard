from __future__ import unicode_literals
from django.db import models
from re import match
import bcrypt

class UserManager(models.Manager):
    def register(self, data):
        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$' 
        NAME_REGEX = r'^[A-z\s]*$'
        errors = []

        if data['first_name'] == '':
            errors.append('First name can not be blank')
        if len(data['first_name']) < 2:
            errors.append('First name must be fewer than 2 characters')
        if not match(NAME_REGEX, data['first_name']):
            errors.append('First name can only contain letters')
        if data['last_name'] == '':
            errors.append('Last name can not be blank')
        if len(data['last_name']) < 2:
            errors.append('Last name must be fewer than 2 characters')
        if not match(NAME_REGEX, data['last_name']):
            errors.append('Last name can only contain letters')
        
        if data['email'] == '':
            errors.append('Email can not be blank')
        if not match(EMAIL_REGEX, data['email']):
            errors.append('Email format invalid')

        if data['password'] == '':
            errors.append('Password can not be blank')
        elif data['password'] != data['password_confirm']:
            errors.append('Passwords must be matching')
        elif data['password'] < 8:
            errors.append('Passwords must be at least 8 characters in length')
        else:
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        if self.filter(email=data['email']):
            errors.append('Email already exists')

        result = {}
        
        if not errors:
            result['created'] = True
            u = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=password, user_level=0)
            u.save()
            result['user'] = u
        else:
            result['created'] = False
            result['errors'] = errors

        return result

    def login(self, data):
        u = self.filter(email=data['email'])
        result = {}
    
        if data['password'] != '' and u and u[0].password == bcrypt.hashpw(data['password'].encode('utf-8'), u[0].password.encode('utf-8')):
            result['success'] = True
            u = u[0]
            result['user_id'] = u.id
            result['first_name'] = u.first_name
            result['last_name'] = u.last_name
            result['user_level'] = u.user_level
        else:
            result['success'] = False

        return result

    def create_user(self, data, is_admin):
        response = {}

        if not is_admin:
            response['created'] = False
            return response
        return self.register(data)

    def delete_user(self, session_user_id, user_id, is_admin):
        response = {}
        
        if not is_admin:
            response['deleted'] = False
            return response
        user = self.get(id=user_id) 

        if user.user_level == 9 or session_user_id == user_id:
            response['deleted'] = False
            return response

        user.delete()
        response['deleted'] = True
        return response

    def update_user(self, session_user_id, user_id, data, is_admin):
        response = { 'updated': False }

        if str(session_user_id) == str(user_id) or is_admin == True:
            kwargs = {}
            user = None

            if 'password' in data:
                if data['password'] == data['password_confirm']:
                    user = self.filter(id=user_id)
                    if user[0].password != bcrypt.hashpw(data['password_old'].encode('utf-8'), user[0].password.encode('utf-8')):
                        return response
                else: 
                    return response

            for k,v in data.iteritems():
                if k not in ['csrfmiddlewaretoken', 'password_old', 'password_confirm']:
                    kwargs[k] = v

            if 'password' in kwargs:
                kwargs['password'] = bcrypt.hashpw(kwargs['password'].encode('utf-8'), bcrypt.gensalt())
            
            if not user:
                user = self.filter(id=user_id)
            user = user.update(**kwargs)
            response['updated'] = True
            response['user'] = user

        return response


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=512, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        db_table = 'users'
