from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blogging.models import Post


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by("-published_date")
    context = {"posts": posts}
    return render(request, "blogging/list.html", context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {"post": post}
    return render(request, "blogging/detail.html", context)


class BlogListView(ListView):
    model = Post
    template_name = "blogging/list.html"
    queryset = Post.objects.order_by("-published_date").exclude(
        published_date__exact=None
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.get_queryset()
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = "blogging/detail.html"

    def post(self, request, *args, **kwargs):
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            raise Http404
        context = {"post": post}
        return render(request, "blogging/detail.html", context)
