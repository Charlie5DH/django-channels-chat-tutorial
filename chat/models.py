from django.contrib.auth.models import User
from django.db import models

# Create your models here.

## in here there is another model named user, it is just imported from Django
## so we can use it in our models.py

''' class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username '''

class Room(models.Model):
    '''
    Room represents a chat room. 
    It contains an online field for tracking when users connect and disconnect from the chat room.
    '''
    name = models.CharField(max_length=255)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        ## count the number if online users
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()
    
    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        ## Name of the room and the number of online users
        return f'{self.name} ({self.get_online_count()})'

class Message(models.Model):
    '''
    Message represents a message sent to the chat room. 
    We'll use this model to store all the messages sent in the chat.
    '''
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'