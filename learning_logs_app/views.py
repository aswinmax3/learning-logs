from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# 🔹 Home page
def index(request):
    topics = Topic.objects.all()
    entries = Entry.objects.all()

    context = {
        'topics': topics,
        'entries': entries
    }
    return render(request, 'learning_logs_app/index.html', context)


# 🔹 List all topics
def topics(request):
    topics = Topic.objects.all()
    return render(request, 'learning_logs_app/topics.html', {'topics': topics})


# 🔹 Topic detail + its entries
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.all().order_by('-date_added')

    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request, 'learning_logs_app/topic.html', context)


# 🔹 Add new topic
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs_app:topics')

    return render(request, 'learning_logs_app/new_topic.html', {'form': form})


# 🔹 Add new entry to a topic
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = topic   # 🔥 link entry to topic
            entry.save()
            return redirect('learning_logs_app:topic', topic_id=topic.id)

    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs_app/new_entry.html', context)


# 🔹 Edit an existing entry
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs_app:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs_app/edit_entry.html', context)