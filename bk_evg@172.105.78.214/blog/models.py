from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now) # auto_now=время каждого исправления
														#auto_now_add=время когда мы это создали
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', args=[self.id])