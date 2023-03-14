from django.db import models

# Create your models here.
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User

class Containers_id(models.Model):
    cid = models.CharField(max_length=100)

    def __str__(self):
        return self.cid

class Container(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pages = models.IntegerField()
    container_id = models.ManyToManyField(Containers_id)


    def __str__(self):
        return self.student

    def get_absolute_url(self):
        return reverse('book_edit', kwargs={'pk': self.pk})