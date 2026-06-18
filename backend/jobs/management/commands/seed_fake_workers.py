import random
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from jobs.models import CandidateProfile, JobRole
from jobs.roles import ROL_APLICACION_TRABAJADOR, asignar_rol_usuario

NOMBRES = [
    "Ana", "Luis", "Carla", "Martin", "Rocio", "Diego", "Valeria", "Pablo", "Julieta", "Marcos",
    "Camila", "Bruno", "Sofia", "Tomas", "Agustina", "Nicolas", "Florencia", "Javier", "Micaela", "Gonzalo",
]

NOMBRES_FEMENINOS = {
    "ana", "carla", "rocio", "valeria", "julieta", "camila", "sofia",
    "agustina", "florencia", "micaela",
}

APELLIDOS = [
    "Garcia", "Perez", "Lopez", "Gomez", "Diaz", "Fernandez", "Sosa", "Romero", "Alvarez", "Torres",
    "Ruiz", "Acosta", "Molina", "Silva", "Castro", "Rojas", "Vega", "Navarro", "Ibarra", "Morales",
]

CIUDADES = [
    "Buenos Aires", "Cordoba", "Rosario", "Mendoza", "La Plata", "Mar del Plata", "Salta", "Santa Fe",
    "Tucuman", "Neuquen", "San Juan", "Resistencia", "Posadas", "Parana", "Corrientes",
]

RUBROS_RESERVA = [
    "Cocinero", "Camarero", "Parrillero", "Pastelero", "Bartender",
    "Barista", "Panadero", "Pizzero", "Encargado de salon", "Ayudantes de cocina",
]

DISPONIBILIDADES = [
    "Full time",
    "Part time",
    "Noches",
    "Fines de semana",
    "Turno manana",
    "Turno tarde",
]

PLANTILLAS_BIO = [
    "Trabajador con enfoque en servicio y calidad en {role}.",
    "Experiencia comprobable en {role} y trabajo en equipo.",
    "Perfil proactivo para tareas de {role} en ritmo de alta demanda.",
    "Compromiso y responsabilidad en funciones de {role}.",
]


def descargar_foto_real():
    """Descarga una foto real de persona desde randomuser.me API."""
    try:
        response = requests.get("https://randomuser.me/api/", timeout=10)
        response.raise_for_status()
        data = response.json()
        photo_url = data["results"][0]["picture"]["large"]
        
        photo_response = requests.get(photo_url, timeout=10)
        photo_response.raise_for_status()
        return photo_response.content
    except Exception as e:
        print(f"Error descargando foto: {e}. Usando placeholder...")
        return None


def construir_svg_chef(is_male=True):
    """Genera SVG de chef estilo restaurante moderno con dos variantes."""
    if is_male:
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640">
<defs>
    <linearGradient id="bgM" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#f2eee8"/>
        <stop offset="100%" stop-color="#ddd4c8"/>
    </linearGradient>
    <linearGradient id="apronM" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#111827"/>
        <stop offset="100%" stop-color="#1f2937"/>
    </linearGradient>
</defs>
<rect width="640" height="640" fill="url(#bgM)"/>
<circle cx="320" cy="320" r="246" fill="#ffffff" opacity="0.72"/>
<ellipse cx="320" cy="122" rx="132" ry="64" fill="#ffffff"/>
<rect x="206" y="122" width="228" height="76" rx="32" fill="#ffffff"/>
<ellipse cx="320" cy="198" rx="114" ry="24" fill="#ececec"/>
<path d="M236 280c0-60 38-106 84-106s84 46 84 106" fill="#2d231b"/>
<circle cx="320" cy="286" r="92" fill="#deb48f"/>
<circle cx="286" cy="286" r="7" fill="#111111"/>
<circle cx="354" cy="286" r="7" fill="#111111"/>
<path d="M290 334c10 8 20 12 30 12s20-4 30-12" fill="none" stroke="#7d4a2e" stroke-width="6" stroke-linecap="round"/>
<path d="M176 620c24-116 92-188 144-188s120 72 144 188" fill="#ffffff"/>
<path d="M236 444h168v174H236z" fill="#f8fafc"/>
<path d="M320 444v174" stroke="#d1d5db" stroke-width="4"/>
<circle cx="298" cy="486" r="6" fill="#9ca3af"/>
<circle cx="342" cy="486" r="6" fill="#9ca3af"/>
<circle cx="298" cy="524" r="6" fill="#9ca3af"/>
<circle cx="342" cy="524" r="6" fill="#9ca3af"/>
<path d="M252 468h136v138H252z" fill="url(#apronM)" opacity="0.95"/>
<path d="M320 470l56 32v86h-112v-86z" fill="#0b1220"/>
<path d="M298 524h44" stroke="#f59e0b" stroke-width="8" stroke-linecap="round"/>
<path d="M108 438l18-14 36 46-18 14z" fill="#8b5e3c"/>
<path d="M158 482l56-44 16 20-56 44z" fill="#cbd5e1"/>
<rect x="500" y="432" width="20" height="154" rx="10" fill="#9ca3af"/>
<path d="M510 394c22 0 40 16 40 36h-80c0-20 18-36 40-36z" fill="#e5e7eb"/>
</svg>'''
    else:
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640">
<defs>
    <linearGradient id="bgF" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#f4ece6"/>
        <stop offset="100%" stop-color="#e6d8cc"/>
    </linearGradient>
    <linearGradient id="apronF" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#7f1d1d"/>
        <stop offset="100%" stop-color="#991b1b"/>
    </linearGradient>
</defs>
<rect width="640" height="640" fill="url(#bgF)"/>
<circle cx="320" cy="320" r="246" fill="#ffffff" opacity="0.74"/>
<ellipse cx="320" cy="122" rx="132" ry="64" fill="#ffffff"/>
<rect x="206" y="122" width="228" height="76" rx="32" fill="#ffffff"/>
<ellipse cx="320" cy="198" rx="114" ry="24" fill="#ececec"/>
<path d="M214 304c0-104 50-160 106-160s106 56 106 160c0 68-20 122-48 166H262c-28-44-48-98-48-166z" fill="#5b3b2d"/>
<circle cx="320" cy="286" r="90" fill="#e8bd98"/>
<circle cx="286" cy="286" r="7" fill="#111111"/>
<circle cx="354" cy="286" r="7" fill="#111111"/>
<path d="M292 334c10 8 18 12 28 12s18-4 28-12" fill="none" stroke="#b91c1c" stroke-width="6" stroke-linecap="round"/>
<path d="M176 620c24-116 92-188 144-188s120 72 144 188" fill="#ffffff"/>
<path d="M236 444h168v174H236z" fill="#f8fafc"/>
<path d="M320 444v174" stroke="#d1d5db" stroke-width="4"/>
<circle cx="298" cy="486" r="6" fill="#9ca3af"/>
<circle cx="342" cy="486" r="6" fill="#9ca3af"/>
<circle cx="298" cy="524" r="6" fill="#9ca3af"/>
<circle cx="342" cy="524" r="6" fill="#9ca3af"/>
<path d="M252 468h136v138H252z" fill="url(#apronF)" opacity="0.95"/>
<path d="M320 470l56 32v86h-112v-86z" fill="#7a1212"/>
<path d="M298 524h44" stroke="#fde68a" stroke-width="8" stroke-linecap="round"/>
<path d="M114 430h12v154h-12z" fill="#8b5e3c"/>
<path d="M104 430h32" stroke="#8b5e3c" stroke-width="8" stroke-linecap="round"/>
<path d="M104 452h32" stroke="#8b5e3c" stroke-width="8" stroke-linecap="round"/>
<path d="M500 436h20v150h-20z" fill="#9ca3af"/>
<path d="M510 394l30 42h-60z" fill="#d1d5db"/>
</svg>'''
    return svg.encode("utf-8")


class Command(BaseCommand):
    help = "Crea 100 trabajadores ficticios con rubros, ciudades e imagen de perfil inventada."

    def handle(self, *args, **options):
        rng = random.Random(20260617)

        roles = list(JobRole.objects.order_by("name"))
        if not roles:
            for role_name in RUBROS_RESERVA:
                JobRole.objects.get_or_create(name=role_name)
            roles = list(JobRole.objects.order_by("name"))

        role_counts = {role.id: rng.randint(4, 10) for role in roles}
        role_sequence = []
        for role in roles:
            role_sequence.extend([role] * role_counts[role.id])

        total_workers = len(role_sequence)
        chef_slots_count = max(1, round(total_workers * 0.03))
        chef_slots = set(rng.sample(range(1, total_workers + 1), k=chef_slots_count))

        created = 0
        updated = 0
        for index, role in enumerate(role_sequence, start=1):
            first_name = rng.choice(NOMBRES)
            last_name = rng.choice(APELLIDOS)
            city = CIUDADES[(index - 1) % len(CIUDADES)]

            username = f"fake_worker_{index:03d}"
            email = f"{username}@example.com"
            password = "Demo12345!"

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save(update_fields=["email", "first_name", "last_name", "password"])
            asignar_rol_usuario(user, ROL_APLICACION_TRABAJADOR)

            profile, _ = CandidateProfile.objects.get_or_create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.gender = "mujer" if first_name.lower() in NOMBRES_FEMENINOS else "hombre"
            profile.phone = f"+54 9 11 5{index:06d}"
            profile.city = city
            profile.role = role
            profile.years_experience = rng.randint(1, 16)
            profile.availability = rng.choice(DISPONIBILIDADES)
            profile.bio = rng.choice(PLANTILLAS_BIO).format(role=role.name.lower())
            if profile.personal_photo:
                profile.personal_photo.delete(save=False)
            profile.save()
            profile.roles.add(role)

            # 97% fotos reales, 3% SVG de chefs.
            is_chef_avatar = index in chef_slots
            
            if is_chef_avatar:
                is_male = index % 2 == 0
                svg_bytes = construir_svg_chef(is_male=is_male)
                avatar_name = f"chefs/{'male_v4' if is_male else 'female_v4'}.svg"
                profile.personal_photo.save(avatar_name, ContentFile(svg_bytes), save=True)
                print(f"  👨‍🍳 {username}: SVG chef {'hombre' if is_male else 'mujer'}")
            else:
                photo_bytes = descargar_foto_real()
                if photo_bytes:
                    avatar_name = f"real/{index:03d}.jpg"
                    profile.personal_photo.save(avatar_name, ContentFile(photo_bytes), save=True)
                else:
                    print(f"  ⚠ No se pudo descargar foto para {username}, omitiendo imagen.")

            if user_created:
                created += 1
            else:
                updated += 1

        # Elimina usuarios fake que sobren de corridas anteriores.
        valid_usernames = {f"fake_worker_{idx:03d}" for idx in range(1, total_workers + 1)}
        extra_users = User.objects.filter(username__startswith="fake_worker_").exclude(username__in=valid_usernames)
        deleted = 0
        for user in extra_users:
            profile = getattr(user, "candidate_profile", None)
            if profile and profile.personal_photo:
                profile.personal_photo.delete(save=False)
            user.delete()
            deleted += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Registros creados: {created}. Registros actualizados: {updated}. Registros eliminados: {deleted}."
            )
        )
        self.stdout.write(self.style.WARNING("✅ 97% fotos reales desde randomuser.me | 3% avatares SVG de chefs (hombre/mujer)"))
        self.stdout.write(self.style.SUCCESS(f"Total generado: {total_workers}. Min por rubro: 4 | Max por rubro: 10"))
