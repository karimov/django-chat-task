from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from chat.serializers import UserListSerializer, UserCreateSerializer, MessageSerializer, LastMessageIdSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.reverse import reverse
from chat.models import Message

import time


def client(request):
	return render(request, "client.html", {})

@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def api_root(request):
	return Response({
			"users": reverse('user-list', request=request),
			"messages": reverse('message-list', request=request)
		}) 

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def user_list(request):
	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserListSerializer(users, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		print(request.data)
		serializer = UserCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes((permissions.IsAdminUser, ))
def user_del(request, pk):
	try:
		user = User.objects.get(pk=pk)
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UserCreateSerializer(user)
		return Response(serializer.data)
	elif request.method == 'DELETE':
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


# Polling
POLLING_INTERVAL = 15

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def poll(request):
	print(request.data)
	mid_serializer = LastMessageIdSerializer(data=request.data)
	if mid_serializer.is_valid():
		last_mid = request.data.get('last_mid', 1)
		for _ in range(POLLING_INTERVAL):
			messages = Message.objects.get_messages(int(last_mid))
			mcount = messages.count()
			if mcount > 30:
				messages = messages[mcount - 30:]
			if mcount == 0:
				time.sleep(1)
				continue

			serializer = MessageSerializer(messages, many=True)
			last_mid = max(m.pk for m in messages)
			return Response({
					"last_mid": last_mid,
					"messages": serializer.data
				})	
		return Response({
				'message': "OK"
				})
	return Response(mid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated, ))
def send(request):
	serializer = MessageSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save(user=request.user)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def message_list(request):
	messages = Message.objects.all()
	serializer = MessageSerializer(messages, many=True)
	return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def message_history(request):
	date = request.GET.get('date', '')
	try:
		messages = Message.objects.message_history(date)
	except ValidationError:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	serializer = MessageSerializer(messages, many=True)
	return Response(serializer.data)
