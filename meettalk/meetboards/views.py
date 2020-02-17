from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meet, Board, Topic, Post
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import NewTopicForm, PostForm
from django.utils.decorators import method_decorator
from django.utils import timezone

def home(request):
    return render(request,"home.html")

class MeetListView(ListView):
    model = Meet
    context_object_name = 'meets'
    template_name = 'meets.html'
    #paginate_by = 20

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards.html'

    def get_context_data(self, **kwargs):
        kwargs['meet'] = self.meet
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.meet = get_object_or_404(Meet, pk = self.kwargs.get('pk'))
        queryset = self.meet.boards.all
        return queryset

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk = self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}.'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views +=1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):     
        #self.topic = get_object_or_404(Topic, board__pk = self.kwargs.get('board_pk'), pk = self.kwargs.get('topic_pk'))
        self.topic = get_object_or_404(Topic, pk = self.kwargs.get('topic_pk'))
    #     print(f"Inside PostListView with board_pk: {self.kwargs.get('board_pk')} and topic_pk: {self.kwargs.get('topic_pk')}")
        print(f"Found this topic: {self.topic}")
        queryset = self.topic.posts.order_by('created_at')
        print("length: ",len(queryset))
        return queryset



@login_required
def new_topic(request, pk, board_pk):
    print("Inside new_topic")
    board = get_object_or_404(Board, pk=board_pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            print("Am I here?? So confusing")
            return redirect('topic_posts', pk=pk, board_pk = board_pk, topic_pk=topic.pk)
    else:
        print("Should be here")
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})

@login_required
def reply_topic(request, pk, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk = topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts', pk=pk, board_pk = board_pk, topic_pk=topic.pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic':topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name  = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by  = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk = post.topic.board.meet.pk, board_pk = post.topic.board.pk, topic_pk=post.topic.pk)