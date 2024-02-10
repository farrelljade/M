from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create a tweet model.
class Tweet(models.Model):
    user = models.ForeignKey(User, related_name="tweets", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "            
            f"({self.created_at:%d-%m-%Y %H:%M}): "            
            f"{self.body}"            
        )

# Create a User Profile Model.
class Profile(models.Model):
    # Link each Profile to a User. If a User is deleted, their Profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Set up a many-to-many relationship to the same model ('self') for followers.
    # 'symmetrical=False' means if A follows B, B doesn't necessarily follow A.
    # 'related_name' allows querying who follows a user.
    # 'blank=True' allows a profile to follow no other profiles.
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    
    # Info on when user last modified their data.
    date_modified = models.DateTimeField(auto_now=True)
    # Image upload for User if want to
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.user.username

# Signal function to create a Profile when a User is created.
# @receiver to connect the 'create_profile' function to the User model's 'post_save' signal.    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Check if it's a new user instance.
    if created:
        # Create a Profile instance for the new user.
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves automatically.
        user_profile.follows.set([instance.profile.id])
        user_profile.save()