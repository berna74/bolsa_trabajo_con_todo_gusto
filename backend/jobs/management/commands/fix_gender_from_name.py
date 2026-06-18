"""
Asigna gender='mujer' a los perfiles cuyo first_name coincide con nombres femeninos conocidos
y que aún tienen gender vacío. Los demás quedan como 'hombre'.
Útil para migrar perfiles creados antes de que existiera el campo gender.
"""
from django.core.management.base import BaseCommand

from jobs.models import CandidateProfile

NOMBRES_FEMENINOS = {
    "ana", "carla", "rocio", "rocío", "valeria", "julieta", "camila", "sofia", "sofía",
    "agustina", "florencia", "micaela", "valentina", "abrina", "eugenia",
}


class Command(BaseCommand):
    help = "Completa el campo gender en perfiles existentes según el nombre."

    def handle(self, *args, **options):
        perfiles = CandidateProfile.objects.filter(gender="")
        mujer = hombre = 0

        for perfil in perfiles:
            nombre = (perfil.first_name or "").strip().lower()
            if nombre in NOMBRES_FEMENINOS:
                perfil.gender = "mujer"
                mujer += 1
            else:
                perfil.gender = "hombre"
                hombre += 1
            perfil.save(update_fields=["gender"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizados {mujer + hombre} perfiles: {mujer} mujer, {hombre} hombre."
            )
        )
