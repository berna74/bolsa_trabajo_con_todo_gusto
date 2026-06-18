from django.contrib.auth.models import Group

ROL_APLICACION_SUPERADMIN = "superadministrador"
ROL_APLICACION_ADMIN = "administrador"
ROL_APLICACION_TRABAJADOR = "trabajador"
ROL_APLICACION_CLIENTE = "cliente"

NOMBRE_GRUPO_ADMIN = "administrador"
NOMBRE_GRUPO_TRABAJADOR = "trabajador"
NOMBRE_GRUPO_CLIENTE = "cliente"

GRUPOS_GESTIONADOS = (
    NOMBRE_GRUPO_ADMIN,
    NOMBRE_GRUPO_TRABAJADOR,
    NOMBRE_GRUPO_CLIENTE,
)

ROLES_REGISTRO_PUBLICO = (
    ROL_APLICACION_TRABAJADOR,
    ROL_APLICACION_CLIENTE,
)


def asegurar_grupos_roles():
    for nombre_grupo in GRUPOS_GESTIONADOS:
        Group.objects.get_or_create(name=nombre_grupo)


def obtener_rol_aplicacion_usuario(user):
    if not user or not user.is_authenticated:
        return None

    if user.is_superuser:
        return ROL_APLICACION_SUPERADMIN

    if user.groups.filter(name=NOMBRE_GRUPO_ADMIN).exists():
        return ROL_APLICACION_ADMIN

    if user.groups.filter(name=NOMBRE_GRUPO_TRABAJADOR).exists():
        return ROL_APLICACION_TRABAJADOR

    if user.groups.filter(name=NOMBRE_GRUPO_CLIENTE).exists():
        return ROL_APLICACION_CLIENTE

    # Compatibilidad con usuarios existentes sin grupo.
    if hasattr(user, "candidate_profile"):
        return ROL_APLICACION_TRABAJADOR

    return ROL_APLICACION_CLIENTE


def asignar_rol_usuario(user, rol_aplicacion):
    if rol_aplicacion == ROL_APLICACION_SUPERADMIN:
        raise ValueError("El rol superadministrador se gestiona con is_superuser.")

    asegurar_grupos_roles()

    rol_a_grupo = {
        ROL_APLICACION_ADMIN: NOMBRE_GRUPO_ADMIN,
        ROL_APLICACION_TRABAJADOR: NOMBRE_GRUPO_TRABAJADOR,
        ROL_APLICACION_CLIENTE: NOMBRE_GRUPO_CLIENTE,
    }

    nombre_grupo = rol_a_grupo.get(rol_aplicacion)
    if nombre_grupo is None:
        raise ValueError(f"Rol invalido: {rol_aplicacion}")

    user.groups.remove(*Group.objects.filter(name__in=GRUPOS_GESTIONADOS))
    user.groups.add(Group.objects.get(name=nombre_grupo))

    if not user.is_superuser:
        user.is_staff = rol_aplicacion == ROL_APLICACION_ADMIN
        user.save(update_fields=["is_staff"])
