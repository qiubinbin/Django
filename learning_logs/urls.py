from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^topics/$', views.topics, name='topics'),
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
	url('^new_topic/$', views.new_topic, name='new_topic'),
	url(r'^new_topic/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry')
]
