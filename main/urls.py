from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('applications/create/', views.create_application, name='create_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
path('my-applications/delete/<int:pk>/', views.delete_application, name='delete_application'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

