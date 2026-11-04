from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from main.models import UserProfile


class Command(BaseCommand):
    help = "Create the default admin and citizen accounts used by the project."

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user, admin_created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@roadportal.local", "is_staff": True, "is_superuser": True},
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email = admin_user.email or "admin@roadportal.local"
        admin_user.set_password("admin123")
        admin_user.save()

        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.is_approved = True
        admin_profile.save()

        citizen_user, citizen_created = User.objects.get_or_create(
            username="citizen",
            defaults={"email": "citizen@roadportal.local", "is_staff": False, "is_superuser": False},
        )
        citizen_user.is_staff = False
        citizen_user.is_superuser = False
        citizen_user.email = citizen_user.email or "citizen@roadportal.local"
        citizen_user.set_password("citizen123")
        citizen_user.save()

        citizen_profile, _ = UserProfile.objects.get_or_create(user=citizen_user)
        citizen_profile.is_approved = True
        citizen_profile.save()

        self.stdout.write(self.style.SUCCESS("Default users are ready: admin/admin123 and citizen/citizen123"))
