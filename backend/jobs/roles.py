from django.contrib.auth.models import Group

APP_ROLE_SUPERADMIN = "superadministrador"
APP_ROLE_ADMIN = "administrador"
APP_ROLE_WORKER = "trabajador"
APP_ROLE_CLIENT = "cliente"

GROUP_NAME_ADMIN = "administrador"
GROUP_NAME_WORKER = "trabajador"
GROUP_NAME_CLIENT = "cliente"

MANAGED_GROUPS = (
    GROUP_NAME_ADMIN,
    GROUP_NAME_WORKER,
    GROUP_NAME_CLIENT,
)

PUBLIC_REGISTRATION_ROLES = (
    APP_ROLE_WORKER,
    APP_ROLE_CLIENT,
)


def ensure_role_groups():
    for group_name in MANAGED_GROUPS:
        Group.objects.get_or_create(name=group_name)


def get_user_app_role(user):
    if not user or not user.is_authenticated:
        return None

    if user.is_superuser:
        return APP_ROLE_SUPERADMIN

    if user.groups.filter(name=GROUP_NAME_ADMIN).exists():
        return APP_ROLE_ADMIN

    if user.groups.filter(name=GROUP_NAME_WORKER).exists():
        return APP_ROLE_WORKER

    if user.groups.filter(name=GROUP_NAME_CLIENT).exists():
        return APP_ROLE_CLIENT

    # Compatibilidad con usuarios existentes sin grupo.
    if hasattr(user, "candidate_profile"):
        return APP_ROLE_WORKER

    return APP_ROLE_CLIENT


def assign_user_role(user, app_role):
    if app_role == APP_ROLE_SUPERADMIN:
        raise ValueError("El rol superadministrador se gestiona con is_superuser.")

    ensure_role_groups()

    role_to_group = {
        APP_ROLE_ADMIN: GROUP_NAME_ADMIN,
        APP_ROLE_WORKER: GROUP_NAME_WORKER,
        APP_ROLE_CLIENT: GROUP_NAME_CLIENT,
    }

    group_name = role_to_group.get(app_role)
    if group_name is None:
        raise ValueError(f"Rol invalido: {app_role}")

    user.groups.remove(*Group.objects.filter(name__in=MANAGED_GROUPS))
    user.groups.add(Group.objects.get(name=group_name))

    if not user.is_superuser:
        user.is_staff = app_role == APP_ROLE_ADMIN
        user.save(update_fields=["is_staff"])
