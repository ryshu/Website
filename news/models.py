from core.cache import invalid_fragment_cache
from django.core.cache import cache
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    picture = models.ImageField(upload_to="news_pictures", null=True, blank=True)
    homepage_highlight = models.BooleanField(default = False)


class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=News)
@receiver(post_delete, sender=News)
@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def cache_profile_handler(sender, **kwargs):
    cache.delete_pattern("template.cache.news_index.*")

