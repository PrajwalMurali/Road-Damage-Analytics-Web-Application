from django.db import migrations


def ensure_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("main", "UserProfile")

    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user, defaults={"is_approved": False})


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_fix_user_approval_state"),
    ]

    operations = [
        migrations.RunPython(ensure_profiles, migrations.RunPython.noop),
    ]
