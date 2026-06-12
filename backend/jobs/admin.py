from django.contrib import admin

from .models import CandidateProfile, JobRole, ProfessionalReference, WorkExperience


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def has_add_permission(self, request):
        return bool(request.user and request.user.is_superuser)

    def has_change_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user and request.user.is_superuser)


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "city", "role", "years_experience")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("profile", "company_name", "role", "start_date", "end_date", "is_current")


@admin.register(ProfessionalReference)
class ProfessionalReferenceAdmin(admin.ModelAdmin):
    list_display = ("profile", "full_name", "relation", "phone", "email")
