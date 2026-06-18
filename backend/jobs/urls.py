from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CategoryItemViewSet,
    CandidateProfileView,
    HealthCheckView,
    JobRoleViewSet,
    MeView,
    PublicWorkersByRoleView,
    ProfessionalReferenceViewSet,
    RegisterView,
    UserManagementViewSet,
    WorkExperienceViewSet,
)

router = DefaultRouter()
router.register("roles", JobRoleViewSet, basename="roles")
router.register("categories", CategoryItemViewSet, basename="categories")
router.register("fichas", CategoryItemViewSet, basename="fichas")
router.register("experiences", WorkExperienceViewSet, basename="experiences")
router.register("references", ProfessionalReferenceViewSet, basename="references")
router.register("users", UserManagementViewSet, basename="users")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("public/workers-by-role/", PublicWorkersByRoleView.as_view(), name="public_workers_by_role"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("profile/", CandidateProfileView.as_view(), name="profile"),
    path("", include(router.urls)),
]
