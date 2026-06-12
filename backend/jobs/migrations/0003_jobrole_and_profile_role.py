from django.db import migrations, models
import django.db.models.deletion


def populate_roles_from_desired_position(apps, schema_editor):
    CandidateProfile = apps.get_model("jobs", "CandidateProfile")
    JobRole = apps.get_model("jobs", "JobRole")

    for profile in CandidateProfile.objects.all().iterator():
        desired_position = (profile.desired_position or "").strip()
        if not desired_position:
            continue

        role, _ = JobRole.objects.get_or_create(name=desired_position)
        profile.role_id = role.id
        profile.save(update_fields=["role"])


def reverse_populate_desired_position(apps, schema_editor):
    CandidateProfile = apps.get_model("jobs", "CandidateProfile")

    for profile in CandidateProfile.objects.select_related("role").all().iterator():
        profile.desired_position = profile.role.name if profile.role_id else ""
        profile.save(update_fields=["desired_position"])


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_candidateprofile_personal_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="candidateprofile",
            name="role",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="profiles", to="jobs.jobrole"),
        ),
        migrations.RunPython(populate_roles_from_desired_position, reverse_populate_desired_position),
        migrations.RemoveField(
            model_name="candidateprofile",
            name="desired_position",
        ),
    ]
