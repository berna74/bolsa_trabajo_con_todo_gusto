from django.conf import settings
from django.db import models


class JobRole(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    TYPE_REQUIREMENT = "requisito"
    TYPE_SKILL = "habilidad"
    TYPE_OTHER = "otro"
    TYPE_CHOICES = (
        (TYPE_REQUIREMENT, "Requisito"),
        (TYPE_SKILL, "Habilidad"),
        (TYPE_OTHER, "Otro"),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["type", "name"]
        unique_together = ("type", "name")
        verbose_name = "Ficha"
        verbose_name_plural = "Fichas"

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"


class CandidateProfile(models.Model):
    GENDER_CHOICES = (
        ("hombre", "Hombre"),
        ("mujer", "Mujer"),
    )
    EDUCATION_CHOICES = (
        ("completo", "Completo"),
        ("incompleto", "Incompleto"),
    )
    SCHEDULE_CHOICES = (
        ("manana", "Mañana"),
        ("tarde", "Tarde"),
        ("noche", "Noche"),
        ("full_time", "Full Time"),
    )
    AVAILABILITY_CHOICES = (
        ("disponible", "Disponible"),
        ("weekends", "Fines de semana"),
        ("holidays", "Feriados"),
        ("full", "Fines de semana y feriados"),
    )
    SKILLS_CHOICES = (
        ("atencion_cliente", "Atención al cliente"),
        ("manejo_bandeja", "Manejo de bandeja"),
        ("caja_cobro", "Caja y cobro"),
        ("cafeteria", "Cafetería"),
        ("cocteleria", "Coctelería"),
        ("cocina_caliente", "Cocina caliente"),
        ("cocina_fria", "Cocina fría"),
        ("pasteleria", "Pastelería"),
        ("manipulacion_alimentos", "Manipulación de alimentos"),
        ("limpieza_orden", "Limpieza y orden de cocina"),
        ("manejo_stock", "Manejo de stock"),
        ("sistemas_gestion", "Sistemas de gestión gastronómica"),
    )

    # Datos personales
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidate_profile")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    personal_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, unique=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    social_networks = models.CharField(max_length=500, blank=True, help_text="LinkedIn, Instagram, Facebook, etc. (opcional)")

    # Puesto al que se postula
    role = models.ForeignKey(JobRole, on_delete=models.PROTECT, null=True, blank=True, related_name="profiles")
    roles = models.ManyToManyField(JobRole, blank=True, related_name="candidate_profiles")

    # Experiencia y disponibilidad
    years_experience = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=120, blank=True)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, blank=True)
    can_work_weekends_holidays = models.BooleanField(default=False)
    expected_salary = models.CharField(max_length=100, blank=True, help_text="Rango salarial pretendido")

    # Formación
    primary_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    secondary_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    tertiary_education = models.BooleanField(default=False, help_text="¿Tiene educación terciaria/universitaria?")
    tertiary_details = models.TextField(blank=True, help_text="Detalle de estudios terciarios/universitarios")
    gastro_courses = models.TextField(blank=True, help_text="Cursos gastronómicos realizados")

    # Conocimientos y habilidades
    skills = models.CharField(max_length=500, blank=True, help_text="Habilidades (separadas por comas o JSON)")

    # Documentos y certificaciones
    has_sanitary_license = models.BooleanField(default=False, help_text="¿Libreta Sanitaria vigente?")
    has_food_handling_cert = models.BooleanField(default=False, help_text="¿Carnet de manipulación de alimentos?")
    has_own_transport = models.BooleanField(default=False, help_text="¿Movilidad propia?")

    # General
    bio = models.TextField(blank=True)
    observations = models.TextField(blank=True, help_text="Observaciones adicionales")

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        verbose_name_plural = "Candidate Profiles"


class WorkExperience(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=160)
    role = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} en {self.company_name}"


class ProfessionalReference(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="references")
    full_name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    relation = models.CharField(max_length=120)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
