from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import PostForm
from .models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"


class PostCreateView(CreateView):
    model_class = Post
    form_class = PostForm
    template_name = "posts/post_edit.html"

    def get_success_url(self, **kwargs):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self, **kwargs):
        return None

    def form_valid(self, form):
        response = {}
        if super().form_valid(form):
            self.object = form.save()
            response = {
                "success": "success",
                "title": self.object.title,
                "text": self.object.text,
            }
        else:
            response = {"error": "Error!"}
        return JsonResponse(response)


class PostDeleteView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_list.html"

    def render_to_response(self, context, **response_kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": "success"})
