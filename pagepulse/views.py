from django.shortcuts import render

def index(request):
    """
    Renders the main frontend HTML page for Page Pulse.
    """
    return render(request, 'index.html')
