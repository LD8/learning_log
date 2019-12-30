from django.shortcuts import render, get_object_or_404, Http404, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    '''home page'''
    return render(request, 'learning_logs/index.html')


def topics(request):
    '''displaying all the topics one has created'''
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_pk):
    '''displaying all the entries under this sepcific topic'''
    topic = get_object_or_404(Topic, pk=topic_pk)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def entry(request, topic_pk, entry_pk):
    '''displaying one specific entry on one page'''
    topic = get_object_or_404(Topic, pk=topic_pk)
    try:
        entry = topic.entry_set.get(pk=entry_pk)
    except:
        raise Http404
    context = {'entry': entry}
    return render(request, 'learning_logs/entry.html', context)


def new_topic(request):
    '''adding a new topic'''
    if request.method != 'POST':
        # create a blank form behind the scene if user just opens the page
        form = TopicForm()
    else:
        # form receives the data behind the scene
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # render the blank form to the page
    # OR display the invalid form / error messages
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_pk):
    '''adding a new entry under a specific topic'''
    # get the correct topic object under which the new entry is created
    topic = get_object_or_404(Topic, pk=topic_pk)
    if request.method != 'POST':
        # create a blank form behind the scene
        form = EntryForm()
    else:
        # form receives the data behind the scene
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_pk=topic_pk)

    # render the blank form or display error
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, topic_pk, entry_pk):
    '''edit an existing entry under a specific topic'''
    # get the correct topic object under which get the correct entry as well
    topic = get_object_or_404(Topic, pk=topic_pk)
    try:
        entry = topic.entry_set.get(pk=entry_pk)
    except:
        raise Http404
    
    if request.method != 'POST':
        # create a blank form and fill in the data from the entry (the instance)
        form = EntryForm(instance=entry)
    else:
        # !!! this is to fill in the existing data and update it with new data received from request.POST !!!
        # but why fill it in again??? can instance=entry be deleted???
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_pk=topic_pk)

    # render the form with existing entry's data
    context = {'form': form, 'topic': topic, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)
