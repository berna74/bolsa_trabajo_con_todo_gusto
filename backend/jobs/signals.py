from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import ensure_role_groups


@receiver(post_migrate)
def setup_default_role_groups(sender, **kwargs):
    if sender.name == "jobs":
        ensure_role_groups()
