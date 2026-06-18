from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import asegurar_grupos_roles


@receiver(post_migrate)
def configurar_grupos_roles_predeterminados(sender, **kwargs):
    if sender.name == "jobs":
        asegurar_grupos_roles()
