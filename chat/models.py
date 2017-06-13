from django.db import models

# Create your models here.

class MessageQuerySet(models.QuerySet):
	def get_messages(self, message_id):
		return self.filter(pk__gt=message_id).order_by('pk')

	def message_history(self, date):
		return self.filter(timestamp__gte=date+' 00:00:00').filter(timestamp__lte=date+ ' 23:59:59')

	def last_message(self):
		count = self.count()
		return self.order_by('pk')[count-1]


class Message(models.Model):
	objects = MessageQuerySet.as_manager()

	user = models.ForeignKey('auth.user', related_name='messages', on_delete=models.CASCADE)
	message = models.CharField(max_length=256)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('timestamp',)

	def __str__(self):
		display = {'id': self.id,
					'username': self.user.username,
					'date': self.timestamp,
					'message': self.message
					}
		return "{id}:{username}:{date}, {message}".format_map(display)