from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from pytils.translit import slugify

from blog.models import Post


class BlogCreateView(CreateView):
    model = Post
    fields = (
        "title",
        "description",
        "image",
        "is_published",
        "author",
    )
    success_url = reverse_lazy("blog:blog")
    extra_context = {"title": "Create Post"}

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Post
    fields = (
        "title",
        "description",
        "image",
        "is_published",
        "author",
    )
    extra_context = {"title": "Update Post"}

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.object.pk])


class BlogListView(ListView):
    model = Post
    extra_context = {"title": "Blog"}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by("-created_at")
        return queryset


class BlogDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post.views_count += 1
        post.save()
        context["title"] = post.title
        return context


class BlogDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:blog")
    extra_context = {"title": "Delete Post"}
