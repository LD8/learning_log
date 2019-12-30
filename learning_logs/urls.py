from django.urls import path
from . import views

app_name="learning_logs"
urlpatterns = [
    path('', views.index, name='index'),
    path('topics', views.topics, name='topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topic_<int:topic_pk>/', views.topic, name='topic'),
    path('topic_<int:topic_pk>/new_entry/', views.new_entry, name='new_entry'),
    path('topic_<int:topic_pk>/entry_<int:entry_pk>/', views.entry, name='entry'),
    path('topic_<int:topic_pk>/entry_<int:entry_pk>/edit_entry', views.edit_entry, name='edit_entry'),
]