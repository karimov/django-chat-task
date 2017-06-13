
from rest_framework import serializers
from chat.models import Message
from django.contrib.auth.models import User

class UserListSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email',)

class UserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'password')

	def create(self, validated_data):
		username = validated_data['username']
		email = '{username}@mail.com'.format(username=username)
		instance = User(username=username, email=email)
		passwd = validated_data['password']
		instance.set_password(passwd)
		instance.save()
		return instance


class LastMessageIdSerializer(serializers.Serializer):
	last_mid = serializers.IntegerField(required=True)

class MessageSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")

	class Meta:
		model = Message
		fields = ('id', 'user', 'message', 'timestamp')

	def create(self, validated_data):
		user= validated_data['user']
		instace = Message.objects.create(user=user, message=validated_data['message'])
		instace.save()
		return instace