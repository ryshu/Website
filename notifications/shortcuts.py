from django.contrib.auth.models import Group, User
from django.db.models import Q
from . import models


def notify(message, backref, backref_args=None, users=None, groups=None, perms=None):
    targets = []

    for group in groups or []:
        targets += list(User.objects.filter(groups__name=group.name).all())

    for perm in perms or []:
        targets += list(User.objects.filter(Q(groups__permissions__codename=perm) | Q(user_permissions__codename=perm) | Q(is_superuser=True)).distinct())

    if users is not None:
        targets += users

    if backref_args:
        backref_args_str = ';'.join(["%s=%s" % (k, v) for k, v in backref_args.items()])
    else:
        backref_args_str = ""

    for user in targets:
        models.Notification.objects.create(
            user=user,
            message=message,
            backref=backref,
            backref_args=backref_args_str,
        )

