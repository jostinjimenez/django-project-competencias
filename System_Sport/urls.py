from django.contrib import admin
from django.urls import path
from django.urls import include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('competitions/', views.competitions, name='competitions'),
]
