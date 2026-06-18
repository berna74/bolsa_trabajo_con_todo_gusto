from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import CandidateProfile, CategoryItem, JobRole, ProfessionalReference, WorkExperience
from .roles import (
    NOMBRE_GRUPO_ADMIN,
    NOMBRE_GRUPO_TRABAJADOR,
    ROL_APLICACION_TRABAJADOR,
    asignar_rol_usuario,
)
from .serializers import (
    SerializadorActualizacionRolUsuario,
    SerializadorCierreSesion,
    SerializadorExperienciaLaboral,
    SerializadorFicha,
    SerializadorPerfilPostulante,
    SerializadorReferenciaProfesional,
    SerializadorRegistro,
    SerializadorRubro,
    SerializadorUsuario,
)


class EsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class EsAdminOSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.groups.filter(name=NOMBRE_GRUPO_ADMIN).exists()


class EsTrabajador(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.groups.filter(name=NOMBRE_GRUPO_TRABAJADOR).exists()


class VistaConjuntoRubros(viewsets.ModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = SerializadorRubro

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [EsAdminOSuperAdmin()]


class VistaConjuntoFichas(viewsets.ModelViewSet):
    queryset = CategoryItem.objects.all()
    serializer_class = SerializadorFicha

    def get_permissions(self):
        return [EsAdminOSuperAdmin()]


class VistaRegistro(generics.CreateAPIView):
    serializer_class = SerializadorRegistro
    permission_classes = [permissions.AllowAny]


class VistaCierreSesion(generics.GenericAPIView):
    serializer_class = SerializadorCierreSesion

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            return Response({"detail": "Refresh token inválido o expirado."}, status=400)

        return Response(status=204)


class VistaUsuarioActual(generics.RetrieveAPIView):
    serializer_class = SerializadorUsuario

    def get_object(self):
        return self.request.user


class VistaPerfilPostulante(generics.RetrieveUpdateAPIView):
    serializer_class = SerializadorPerfilPostulante
    permission_classes = [EsTrabajador]

    def get_object(self):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return profile


class VistaConjuntoExperienciasLaborales(viewsets.ModelViewSet):
    serializer_class = SerializadorExperienciaLaboral
    permission_classes = [EsTrabajador]

    def get_queryset(self):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return WorkExperience.objects.filter(profile=profile)

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class VistaConjuntoReferenciasProfesionales(viewsets.ModelViewSet):
    serializer_class = SerializadorReferenciaProfesional
    permission_classes = [EsTrabajador]

    def get_queryset(self):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return ProfessionalReference.objects.filter(profile=profile)

    def perform_create(self, serializer):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class VistaChequeoSalud(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "contodogusto-bolsa-api"})


class VistaTrabajadoresPublicosPorRubro(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        profiles = (
            CandidateProfile.objects.select_related("user", "role")
            .prefetch_related("roles", "experiences", "references")
            .all()
            .order_by("last_name", "first_name")
        )
        grouped = {}

        for profile in profiles:
            worker_roles = list(profile.roles.all()) or ([profile.role] if profile.role_id else [])
            if not worker_roles:
                continue

            full_name = f"{profile.first_name} {profile.last_name}".strip() or profile.user.username
            worker_payload = {
                "id": profile.id,
                "full_name": full_name,
                "gender": profile.gender,
                "personal_photo_url": request.build_absolute_uri(profile.personal_photo.url) if profile.personal_photo else "",
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "birth_date": profile.birth_date,
                "address": profile.address,
                "phone": profile.phone,
                "email": profile.user.email,
                "city": profile.city,
                "social_networks": profile.social_networks,
                "years_experience": profile.years_experience,
                "availability": profile.availability,
                "schedule": profile.schedule,
                "can_work_weekends_holidays": profile.can_work_weekends_holidays,
                "expected_salary": profile.expected_salary,
                "primary_education": profile.primary_education,
                "secondary_education": profile.secondary_education,
                "tertiary_education": profile.tertiary_education,
                "tertiary_details": profile.tertiary_details,
                "gastro_courses": profile.gastro_courses,
                "skills": profile.skills,
                "has_sanitary_license": profile.has_sanitary_license,
                "has_food_handling_cert": profile.has_food_handling_cert,
                "has_own_transport": profile.has_own_transport,
                "bio": profile.bio,
                "observations": profile.observations,
                "rubros": [role.name for role in worker_roles],
                "experiences": [
                    {
                        "company_name": exp.company_name,
                        "role": exp.role,
                        "start_date": exp.start_date,
                        "end_date": exp.end_date,
                        "is_current": exp.is_current,
                        "description": exp.description,
                    }
                    for exp in profile.experiences.all()
                ],
                "references": [
                    {
                        "full_name": ref.full_name,
                        "company": ref.company,
                        "relation": ref.relation,
                        "phone": ref.phone,
                        "email": ref.email,
                        "note": ref.note,
                    }
                    for ref in profile.references.all()
                ],
            }

            for role in worker_roles:
                if role.name not in grouped:
                    grouped[role.name] = []
                grouped[role.name].append(worker_payload)

        response = [{"rubro": rubro, "workers": workers} for rubro, workers in grouped.items()]
        return Response(response)


class VistaConjuntoGestionUsuarios(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = SerializadorUsuario
    permission_classes = [EsAdminOSuperAdmin]

    @action(detail=True, methods=["patch"], url_path="role")
    def actualizar_rol(self, request, pk=None):
        target_user = self.get_object()

        if target_user.is_superuser and not request.user.is_superuser:
            raise PermissionDenied("Solo un superadministrador puede modificar otro superadministrador.")

        serializer = SerializadorActualizacionRolUsuario(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_role = serializer.validated_data["app_role"]

        asignar_rol_usuario(target_user, new_role)
        if new_role == ROL_APLICACION_TRABAJADOR:
            CandidateProfile.objects.get_or_create(user=target_user)

        return Response(SerializadorUsuario(target_user).data)
