from django.urls import path
from . import views

app_name="learning_logs"
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),

    # use the same view function, however, 
    # called different name for different functionality i.e. an optional argument in this case
    path('topics/edit/', views.edit_topics, name='edit_topics'),
    path('topics/edit/<int:topic_pk>', views.edit_topics, name='edit_topic'),
    
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topic_<int:topic_pk>/', views.topic, name='topic'),

    # url to edit a topic page, editing the topic or deleting entries under that topic
    path('topic_<int:topic_pk>/edit/', views.edit_topic_page, name='edit_topic_page'),
    path('topic_<int:topic_pk>/edit/<int:entry_pk>', views.edit_topic_page, name='edit_topic_page_entry'),

    path('topic_<int:topic_pk>/new_entry/', views.new_entry, name='new_entry'),
    path('topic_<int:topic_pk>/entry_<int:entry_pk>/', views.entry, name='entry'),
    path('topic_<int:topic_pk>/entry_<int:entry_pk>/edit_entry/', views.edit_entry, name='edit_entry'),
]