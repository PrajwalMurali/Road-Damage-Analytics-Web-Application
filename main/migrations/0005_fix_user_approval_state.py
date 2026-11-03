from django.db import migrations


def reset_non_staff_approvals(apps, schema_editor):
    UserProfile = apps.get_model("main", "UserProfile")
    UserProfile.objects.filter(user__is_staff=False).update(is_approved=False)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_userprofile"),
    ]

    operations = [
        migrations.RunPython(reset_non_staff_approvals, migrations.RunPython.noop),
    ]
