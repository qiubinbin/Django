from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
	"""主页"""
	return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
	"""获取当前用户的主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('data_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	# 确认主题属于当前主题
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('data_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
	"""添加新主题"""
	if request.method != 'POST':
		# 未提交数据，创建一个新表
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


@login_required
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


@login_required
def edit_entry(request, entry_id):
	"""编辑条目"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	# 确认主题属于当前主题
	if topic.owner != request.user:
		raise Http404
	if request.method != 'POST':
		# 使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)
