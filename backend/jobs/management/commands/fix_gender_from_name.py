"""
Asigna gender='mujer' a los perfiles cuyo first_name coincide con nombres femeninos conocidos
y que aún tienen gender vacío. Los demás quedan como 'hombre'.
Útil para migrar perfiles creados antes de que existiera el campo gender.
"""
from django.core.management.base import BaseCommand

from jobs.models import CandidateProfile

FEMALE_FIRST_NAMES = {
    "ana", "carla", "rocio", "rocío", "valeria", "julieta", "camila", "sofia", "sofía",
    "agustina", "florencia", "micaela", "valentina", "abrina", "eugenia",
}


class Command(BaseCommand):
    help = "Completa el campo gender en perfiles existentes según el nombre."

    def handle(self, *args, **options):
        profiles = CandidateProfile.objects.filter(gender="")
        mujer = hombre = 0

        for profile in profiles:
            name = (profile.first_name or "").strip().lower()
            if name in FEMALE_FIRST_NAMES:
                profile.gender = "mujer"
                mujer += 1
            else:
                profile.gender = "hombre"
                hombre += 1
            profile.save(update_fields=["gender"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizados {mujer + hombre} perfiles: {mujer} mujer, {hombre} hombre."
            )
        )
