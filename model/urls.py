from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
#path('admin/', admin.site.urls),
path('',views.main,name='main'),
#path('register',views.register),
path('login/',views.login,name='login'),
path('logout/',views.logoutp,name='logout'),
#path('home',views.home,name='home'),    
#path('admin/', admin.site.urls),
#path('register',views.register,name='register')    
path('register/', views.register, name='register'),
#path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
#path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
path('index/', views.index, name='index'),
path('predict/', views.predict, name='predict'),
path('main1/',views.main1,name='main1'),
path('user_records/', views.user_records, name='user_records'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
