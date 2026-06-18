from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    VistaChequeoSalud,
    VistaCierreSesion,
    VistaConjuntoExperienciasLaborales,
    VistaConjuntoFichas,
    VistaConjuntoGestionUsuarios,
    VistaConjuntoReferenciasProfesionales,
    VistaConjuntoRubros,
    VistaPerfilPostulante,
    VistaRegistro,
    VistaTrabajadoresPublicosPorRubro,
    VistaUsuarioActual,
)

enrutador = DefaultRouter()
enrutador.register("roles", VistaConjuntoRubros, basename="roles")
enrutador.register("categories", VistaConjuntoFichas, basename="categories")
enrutador.register("fichas", VistaConjuntoFichas, basename="fichas")
enrutador.register("experiences", VistaConjuntoExperienciasLaborales, basename="experiences")
enrutador.register("references", VistaConjuntoReferenciasProfesionales, basename="references")
enrutador.register("users", VistaConjuntoGestionUsuarios, basename="users")

urlpatterns = [
    path("health/", VistaChequeoSalud.as_view(), name="health"),
    path("public/workers-by-role/", VistaTrabajadoresPublicosPorRubro.as_view(), name="public_workers_by_role"),
    path("auth/register/", VistaRegistro.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", VistaCierreSesion.as_view(), name="logout"),
    path("auth/me/", VistaUsuarioActual.as_view(), name="me"),
    path("profile/", VistaPerfilPostulante.as_view(), name="profile"),
    path("", include(enrutador.urls)),
]
