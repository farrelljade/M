from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def home(request):
    return render(request, "m/home.html", {})


def profile_list(request):
    if request.user.is_authenticated:
        """Retrieve a list of profiles excluding the users profile."""
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'm/profile_list.html', {'profiles': profiles})
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect('m:home')
    

def profile(request, pk):
    """User profile page."""
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'm/profile.html', {'profile': profile})
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect('m:home')
