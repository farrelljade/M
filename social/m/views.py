from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm

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
    logout(request)
    messages.success(request, "You have logged out...")
    return redirect('m:home')


def user_register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome to M!")
            return redirect('m:home')
        else:
            messages.warning(request, "Registration failed. Please try again...")

            return render(request, 'm/home.html', {'form': form})
        

def update_user(request):
    """User profile update page."""
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        # Get forms.
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Your profile has been updated...")
            return redirect('m:home')
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'm/update_user.html', context)
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('m:home')
