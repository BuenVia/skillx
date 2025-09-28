from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} - {self.client_name}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.user.username} ({self.client.client_name})"
    

class CpdInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    type_course = models.CharField(max_length=200)
    description = models.TextField(null=True)
    date_start = models.DateField()
    date_complete = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=10, null=True)
    grade = models.CharField(max_length=45, null=True)

    def __str__(self):
        return f"{self.user.id} - {self.user.last_name} - {self.title}"
