from django.conf.urls import url,include

urlpatterns = [
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^', include('apps.login_register.urls', namespace='login_register')),
]
