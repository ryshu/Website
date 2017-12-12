from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from notifications.shortcuts import notify
from . import forms
from . import models
import json


def index(request):
    context = {
        'news': models.News.objects.order_by('pub_date').all().reverse().select_related('author__profile').annotate(nb_comments=Count('comments'))[:10],
    }
    return render(request, "news/index.html", context)


@permission_required('news.add_news')
def create(request):
    context = {}

    if request.method == "POST":
        form = forms.NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            form.save()
            return redirect(reverse('news:index'))
        else:
            context['form'] = form

    else:
        context['form'] = forms.NewsForm()

    return render(request, "news/create.html", context)


@permission_required('news.change_news')
def edit(request, nid):
    n = get_object_or_404(models.News, id=nid)
    if request.method == "POST":
        form = forms.NewsForm(request.POST, request.FILES , instance=n)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:index'))
    else:
        form = forms.NewsForm(instance=n)
    context = {'form': form, 'news': n}
    return render(request, "news/edit.html", context)


@permission_required('news.delete_news')
def delete(request, nid):
    n = get_object_or_404(models.News, id=nid)
    n.delete()
    return redirect(reverse('news:index'))


@login_required
def comment(request, nid):
    n = get_object_or_404(models.News, id=nid)
    coms = models.Comment.objects.filter(news=n).select_related('user__profile')
    context = {"news": n, "comments": coms}

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = n
            comment.user = request.user
            comment.save()
            notify(
                "Un commentaire a été posté sur une news",
                "news:comment", {'nid': n.id},
                [n.author]
            )
    else:
        form = forms.CommentForm()
    context['comment_form'] = form
    return render(request, "news/comment.html", context)


@login_required
def del_comment(request, cid):
    if request.user.has_perm('news.delete_comment'):
        c = get_object_or_404(models.Comment, id=cid)
    else:
        c = get_object_or_404(models.Comment, id=cid, user=request.user)
    red = c.news_id
    c.delete()
    return redirect(reverse('news:comment', kwargs={'nid': red}))

