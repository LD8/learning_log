from django.shortcuts import render, get_object_or_404, Http404, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    '''home page'''
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    '''displaying all the topics one has created'''
    # screening to display topics only belongs to the current user
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_pk):
    '''displaying all the entries under this sepcific topic'''
    topic = get_object_or_404(Topic, pk=topic_pk)
    # check if the topic's owner is the logged-in user
    if request.user != topic.owner:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def entry(request, topic_pk, entry_pk):
    '''displaying one specific entry on one page'''
    topic = get_object_or_404(Topic, pk=topic_pk)
    # check if the topic's owner is the logged-in user
    if request.user != topic.owner:
        raise Http404
    try:
        entry = topic.entry_set.get(pk=entry_pk)
    except:
        raise Http404
    context = {'entry': entry}
    return render(request, 'learning_logs/entry.html', context)


@login_required
def new_topic(request):
    '''adding a new topic'''
    if request.method != 'POST':
        # create a blank form behind the scene if user just opens the page
        form = TopicForm()
    else:
        # form receives the data behind the scene
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # render the blank form to the page
    # OR display the invalid form / error messages
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
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


@login_required
def edit_entry(request, topic_pk, entry_pk):
    '''edit an existing entry under a specific topic'''
    # get the correct topic object under which get the correct entry as well
    topic = get_object_or_404(Topic, pk=topic_pk)
    # check if the topic's owner is the logged-in user
    if request.user != topic.owner:
        raise Http404
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


@login_required
def edit_topics(request, topic_pk=None):
    '''edit existing topics mainly the names'''
    # modify the model data according to the request method and name
    if request.method == 'POST' and topic_pk:
        if 'save' in request.POST:
            topic_to_change = get_object_or_404(Topic, pk=topic_pk)
            form = TopicForm(instance=topic_to_change, data=request.POST)
            if form.is_valid():
                form.save()
        elif 'delete' in request.POST:
            topic_to_delete = get_object_or_404(Topic, pk=topic_pk)
            topic_to_delete.delete()
        return redirect('learning_logs:edit_topics')

    # get the original/modified data (which only belongs to the current user) passing to render
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    topic_lst = []
    for topic in topics:
        form = TopicForm(instance=topic)
        topic_lst.append(form)
    context = {'topics': topics, 'topic_lst': topic_lst}
    return render(request, 'learning_logs/edit_topics.html', context)
