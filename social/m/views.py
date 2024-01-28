from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet

def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by("-created_at")  # get tweets from latest to oldest with "-created_at".
    return render(request, "m/home.html", {'tweets': tweets})


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
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")  # get tweets from latest to oldest with "-created_at".
        profile = Profile.objects.get(user_id=pk)
        # Post form logic.
        if request.method == 'POST':
            # Get current user ID
            current_user = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow.
            if action == "unfollow":
                current_user.follows.remove(profile)
            elif action == "follow":
                current_user.follows.add(profile)
            # Save the profile.
            current_user.save()

        context = {
            'tweets': tweets,
            'profile': profile
        }

        return render(request, 'm/profile.html', context)
    else:
        messages.error(request, "You must be logged in to view this page...")
        return redirect('m:home')
