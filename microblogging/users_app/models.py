from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# class User(models.Model):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=180, unique=True)
#     password = models.CharField(max_length=255)
#     bio = models.TextField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.username

# class User(models.Model):
#     bio = models.TextField(max_length=500)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    bio = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follower_followed'),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError("Users cannot follow themselves.")


class Tag(models.Model):
    tag = models.CharField(max_length=180)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts")
    parent_id = models.IntegerField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)