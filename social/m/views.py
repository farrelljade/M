from django.shortcuts import render
from .models import Profile

def home(request):
    return render(request, "m/home.html", {})


def profile_list(request):
    # Retrieve a list of profiles excluding the users profile
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'm/profile_list.html', {'profiles': profiles})