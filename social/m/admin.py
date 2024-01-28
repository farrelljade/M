from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet


# Unregister Groups
admin.site.unregister(Group)


# Mix profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

    
# Extend User model.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial User.
admin.site.unregister(User)

# Reregister User and Profile.
admin.site.register(User, UserAdmin)

# Register Tweets.
admin.site.register(Tweet)