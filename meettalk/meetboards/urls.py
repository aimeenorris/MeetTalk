from django.urls import path
from . import views

urlpatterns = [
    path('', views.MeetListView.as_view(), name='home'),
    path('<int:pk>', views.BoardListView.as_view(), name='meet_boards'),
    path('<int:pk>/boards/<int:board_pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('<int:pk>/boards/<int:board_pk>/new/', views.new_topic, name='new_topic'),
    path('<int:pk>/boards/<int:board_pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('<int:pk>/boards/<int:board_pk>/topics/<int:topic_pk>/',views.PostListView.as_view(), name='topic_posts'),
    path('<int:pk>/boards/<int:board_pk>/topics/<int:topic_pk>/posts/<int:post_pk>', views.PostUpdateView.as_view(), name='edit_post'),
]
