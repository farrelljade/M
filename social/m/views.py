from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm

def home(request):
    tweet = None  # Initialize tweet
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your tweet has been successfully posted...")
                return redirect('m:home')

        context = {
            'form': form,
            'tweet': tweet  # Include tweet only if it's defined
        }

        tweets = Tweet.objects.all().order_by("-created_at")
        context['tweets'] = tweets  # Add tweets to the context
        return render(request, "m/home.html", context)

    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        context = {
            'tweets': tweets  # Add tweets to the context
        }
        return render(request, "m/home.html", context)



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


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully...")
            return redirect('m:home')
        else:
            messages.error(request, "Incorrect login details. Please try again.")
            context = {}
            return render(request, 'm/home.html', context)

def user_logout(request):
    pass