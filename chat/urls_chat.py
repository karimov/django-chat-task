
from django.conf.urls import url, include

from chat import views

# API endpoints

urlpatterns = [
	url(r'^$', views.api_root),
	url(r'^client/$', views.client, name='client'),
	url(r'^users/$', views.user_list, name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.user_del, name='user-del'),
	url(r'^messages/$', views.message_list, name='message-list'),
	url(r'^messages/history/$', views.message_history, name='message-history'),

	url(r'^messages/send$', views.send, name='send'),
	url(r'^messages/poll$', views.poll, name='poll'),

]

urlpatterns += [
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]