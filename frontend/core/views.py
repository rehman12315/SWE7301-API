# US-14: Django Website - Basic Views
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """Simple view to test Django is running"""
    return JsonResponse({
        'status': 'success',
        'message': 'Django is running!',
        'project': 'GeoScope Analytics - US-14'
    })


def home(request):
    """Serve the static HTML page"""
    return render(request, 'index.html')
