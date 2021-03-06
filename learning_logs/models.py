from django.db import models


# Create your models here.
class Topic(models.Model):
	text = models.CharField(max_length=100)
	data_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text


class Entry(models.Model):
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	data_added = models.DateTimeField(auto_now_add=True)

	class Meta():
		verbose_name_plural = 'Entries'

	def __str__(self):
		if len(self.text) >= 50:
			return self.text[:50] + '...'
		else:
			return self.text