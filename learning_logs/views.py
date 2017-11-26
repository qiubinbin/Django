from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Topic
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
	"""主页"""
	return render(request, 'learning_logs/index.html')


def topics(request):
	"""主题"""
	topics = Topic.objects.order_by('data_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('data_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
	"""添加新主题"""
	if request.method != 'POST':
		# 未提交数据，创建一个新表
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
	"""特定主题添加新条目"""
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)
