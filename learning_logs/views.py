from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry

# Create your views here.


def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    entries = topic.entry_set.all()
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    context = {'entry': entry}
    return render(request, 'learning_logs/entry.html', context)
