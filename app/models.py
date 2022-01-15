from django.contrib.auth.models import User
from django.db import models


class Wish(models.Model):
	text = models.TextField(max_length=1000)
	link = models.URLField(verbose_name="Link", null=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	wish_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_of")
	reserved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reserved_wish", null=True)


class Group(models.Model):
	name = models.TextField(max_length=100)
	users = models.ManyToManyField(User, related_name='wish_groups')

	def __str__(self):
		return "<Group {}>".format(self.name)
