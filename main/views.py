from django.shortcuts import render
from .models import Application

def index(request):
    applications_in_progress_count = Application.objects.filter(status='in_progress').count()

    completed_applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]

    context = {
        'applications_in_progress_count': applications_in_progress_count,
        'completed_applications': completed_applications,
    }
    return render(request, 'index.html', context)