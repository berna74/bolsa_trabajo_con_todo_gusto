from django.contrib import admin

from .models import CandidateProfile, CategoryItem, JobRole, ProfessionalReference, WorkExperience


@admin.register(JobRole)
class AdministracionRubro(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def has_add_permission(self, request):
        return bool(request.user and request.user.is_superuser)

    def has_change_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)


@admin.register(CategoryItem)
class AdministracionFicha(admin.ModelAdmin):
    list_display = ("type", "name", "is_active")
    list_filter = ("type", "is_active")
    search_fields = ("name", "description")

    def has_add_permission(self, request):
        return bool(request.user and request.user.is_superuser)

    def has_change_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)


@admin.register(CandidateProfile)
class AdministracionPerfilPostulante(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city", "rubro_principal", "years_experience", "has_sanitary_license", "has_food_handling_cert")
    filter_horizontal = ("roles",)
    search_fields = ("user__username", "first_name", "last_name", "dni", "email")
    fieldsets = (
        ("Datos Personales", {
            "fields": ("user", "first_name", "last_name", "dni", "birth_date", "personal_photo", "address", "city", "phone", "social_networks")
        }),
        ("Puesto al que se postula", {
            "fields": ("role", "roles")
        }),
        ("Experiencia", {
            "fields": ("years_experience", "availability", "schedule", "can_work_weekends_holidays", "expected_salary")
        }),
        ("Formación", {
            "fields": ("primary_education", "secondary_education", "tertiary_education", "tertiary_details", "gastro_courses")
        }),
        ("Conocimientos y Habilidades", {
            "fields": ("skills",)
        }),
        ("Documentos y Certificaciones", {
            "fields": ("has_sanitary_license", "has_food_handling_cert", "has_own_transport")
        }),
        ("Información General", {
            "fields": ("bio", "observations")
        }),
    )

    def rubro_principal(self, obj):
        if obj.role_id:
            return obj.role.name
        first_role = obj.roles.first()
        return first_role.name if first_role else ""

    rubro_principal.short_description = "Rubro principal"


@admin.register(WorkExperience)
class AdministracionExperienciaLaboral(admin.ModelAdmin):
    list_display = ("profile", "company_name", "role", "start_date", "end_date", "is_current")


@admin.register(ProfessionalReference)
class AdministracionReferenciaProfesional(admin.ModelAdmin):
    list_display = ("profile", "full_name", "relation", "phone", "email")
