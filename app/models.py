from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:30]

