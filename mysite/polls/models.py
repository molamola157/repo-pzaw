from django.db import models
from django.contrib.auth.models import AbstractUser


from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
 
    pass





User = get_user_model()  

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
   
    voters = models.ManyToManyField(User, through='Vote', related_name='votes')

    def score(self):
        return self.likes - self.dislikes  
    def __str__(self):
        return self.title




class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('like', 'like'), ('dislike', 'dislike')])

    class Meta: #polub/niepolub raz
        unique_together = ('user', 'post') 

        