#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name   = models.CharField(max_length=30)
	admins = models.ManyToManyField(User)
	
class Topic(models.Model):
	subject   = models.CharField(max_length=1024)
	content   = models.TextField()
	num_views = models.IntegerField(default=1)
	num_replys = models.IntegerField(default=0)
	category  = models.ForeignKey(Category)
	author    = models.ForeignKey(User)
	created   = models.DateTimeField(auto_now=True)
	updated   = models.DateTimeField(auto_now=True)
	last_date = models.DateTimeField(auto_now=True)
	def _get_photo(self):
		p = UserProfile.objects.get(user=self.author)
		return p
	p = property(_get_photo)
	
class Reply(models.Model):
	content = models.TextField()
	author  = models.ForeignKey(User)
	topic   = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	def _get_photo(self):
		p = UserProfile.objects.get(user=self.author)
		return p
	p = property(_get_photo)


class UserProfile(models.Model):
	photo = models.ImageField(upload_to='photo',blank=True, null=True)		#No modle named image 解决方法，easy_install PIL
	nick = models.CharField(max_length=64,blank=True, null=True)
	qq = models.CharField(max_length=32,blank=True, null=True)
	email = models.CharField(max_length=1024,blank=True,null=True)          #blank 可不填空格  Null可以不填
	user = models.ForeignKey(User, unique=True)
	def	_get_photo(self):	
		if self.photo:
			return self.photo
		else:
			image = Defaultimg.objects.filter(desc="avatar").order_by('?')
			if len(image):
				return image[0].img
			else:
				return	'1.jpg'
	get_photo = property(_get_photo)

class Defaultimg(models.Model):
	img = models.ImageField(upload_to='picture',blank=True, null=True)
	desc = models.CharField(max_length=64,blank=True,null=True)
