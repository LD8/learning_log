from django.urls import path
from . import views

app_name="learning_logs"
urlpatterns = [
    path('', views.index, name='index'),
    path('topics', views.topics, name='topics'),
    path('topic_<int:topic_pk>/', views.topic, name='topic'),
    path('entry_<int:entry_pk>/', views.entry, name='entry'),
    # path('topic_<int:topic_pk>/entry_<int:entry_pk>/', views.entry, name='entry'),
]