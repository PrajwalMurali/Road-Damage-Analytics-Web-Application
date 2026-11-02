from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .models import RoadDamageReport, UserProfile


def home(request):
    return render(request, "main/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or ""

        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile = getattr(user, "profile", None)
            if user.is_staff:
                login(request, user)
                return redirect("admin_dashboard")
            if profile is None or not profile.is_approved:
                logout(request)
                return render(
                    request,
                    "main/login.html",
                    {"error": "Your account is waiting for admin approval.", "next": next_url},
                )
            login(request, user)
            return redirect(next_url or "complaint_create")

        return render(
            request,
            "main/login.html",
            {"error": "Invalid username or password.", "next": next_url},
        )

    return render(request, "main/login.html", {"next": request.GET.get("next", "")})


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not username or not email or not password1 or not password2:
            return render(request, "main/register.html", {"error": "Please fill in all fields."})

        if password1 != password2:
            return render(request, "main/register.html", {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, "main/register.html", {"error": "That username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, "main/register.html", {"error": "That email is already registered."})

        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user, is_approved=False)
        messages.success(request, "Registration successful. Please wait for admin approval.")
        return redirect("login")

    return render(request, "main/register.html")


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = User.objects.filter(email=email).first()
        if user:
            reset_link = f"Password reset requested for {user.username}. Contact admin for reset support." 
            send_mail(
                "Road Portal Password Reset",
                f"Hello {user.username},\n\n{reset_link}\n\nPlease contact the system administrator to complete password reset.",
                "noreply@roadportal.local",
                [email],
                fail_silently=True,
            )
            messages.success(request, "Password reset instructions have been sent to your email.")
        else:
            messages.error(request, "No account found with that email address.")
        return redirect("login")

    return render(request, "main/password_reset.html")


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    reports = RoadDamageReport.objects.all()
    stats = [
        {"name": "Total Reports", "value": reports.count()},
        {"name": "High Severity", "value": reports.filter(severity="High").count()},
        {"name": "Pending", "value": reports.filter(status="Pending").count()},
        {"name": "Resolved", "value": reports.filter(status="Resolved").count()},
    ]
    recent_reports = reports.order_by("-reported_at")[:5]
    pending_users = UserProfile.objects.filter(is_approved=False).select_related("user")
    return render(
        request,
        "main/admin_dashboard.html",
        {"stats": stats, "recent_reports": recent_reports, "pending_users": pending_users},
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_user(request, user_id):
    profile = get_object_or_404(UserProfile, user_id=user_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.user.username} has been approved.")
    return redirect("admin_dashboard")


def analytics(request):
    reports = RoadDamageReport.objects.all()
    total_reports = reports.count()
    status_order = ["Pending", "In Progress", "Resolved"]
    severity_order = ["Low", "Medium", "High"]

    data = [
        {"name": "Total Reports", "value": total_reports},
        {"name": "High Severity", "value": reports.filter(severity="High").count()},
        {"name": "Pending", "value": reports.filter(status="Pending").count()},
        {"name": "Resolved", "value": reports.filter(status="Resolved").count()},
    ]

    status_breakdown = []
    for status in status_order:
        count = reports.filter(status=status).count()
        percentage = round((count / total_reports) * 100) if total_reports else 0
        status_breakdown.append({
            "label": status,
            "value": count,
            "percentage": percentage,
        })

    severity_breakdown = []
    for severity in severity_order:
        count = reports.filter(severity=severity).count()
        percentage = round((count / total_reports) * 100) if total_reports else 0
        severity_breakdown.append({
            "label": severity,
            "value": count,
            "percentage": percentage,
        })

    recent_reports = reports.order_by("-reported_at")[:5]
    return render(
        request,
        "main/analytics.html",
        {
            "stats": data,
            "recent_reports": recent_reports,
            "status_breakdown": status_breakdown,
            "severity_breakdown": severity_breakdown,
        },
    )


def report(request):
    reports = RoadDamageReport.objects.all().order_by("-reported_at")
    total_reports = reports.count()
    status_order = ["Pending", "In Progress", "Resolved"]

    progress_cards = []
    for status in status_order:
        count = reports.filter(status=status).count()
        percentage = round((count / total_reports) * 100) if total_reports else 0
        progress_cards.append({
            "label": status,
            "value": count,
            "percentage": percentage,
        })

    resolved_percentage = round((reports.filter(status="Resolved").count() / total_reports) * 100) if total_reports else 0
    active_report_count = reports.filter(status="In Progress").count()
    pending_report_count = reports.filter(status="Pending").count()

    report_items = []
    for item in reports[:5]:
        report_items.append(
            {
                "road_name": item.road_name,
                "reporter_name": item.reporter_name,
                "severity": item.severity,
                "status": item.status,
                "location": item.location,
                "damage_type": item.damage_type,
                "date": item.reported_at.date(),
            }
        )

    return render(
        request,
        "main/report.html",
        {
            "reports": reports[:5],
            "report_items": report_items,
            "progress_cards": progress_cards,
            "resolved_percentage": resolved_percentage,
            "active_report_count": active_report_count,
            "pending_report_count": pending_report_count,
            "total_reports": total_reports,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def complaint_list(request):
    complaints = RoadDamageReport.objects.all().order_by("-reported_at")
    return render(request, "main/complaint_list.html", {"complaints": complaints})


@login_required
def complaint_create(request):
    if request.method == "POST":
        reporter_name = request.POST.get("reporter_name")
        phone_number = request.POST.get("phone_number")
        location = request.POST.get("location")
        road_name = request.POST.get("road_name")
        damage_type = request.POST.get("damage_type")
        severity = request.POST.get("severity")
        description = request.POST.get("description")
        status = request.POST.get("status")
        photo = request.FILES.get("photo")

        if reporter_name and phone_number and location and road_name and damage_type and description:
            RoadDamageReport.objects.create(
                reporter_name=reporter_name,
                phone_number=phone_number,
                location=location,
                road_name=road_name,
                damage_type=damage_type,
                severity=severity or "Medium",
                description=description,
                status=status or "Pending",
                photo=photo,
            )
            return redirect("complaint_list")

    return render(request, "main/complaint_form.html")


@login_required
@user_passes_test(lambda u: u.is_staff)
def complaint_update(request, id):
    complaint = get_object_or_404(RoadDamageReport, id=id)

    if request.method == "POST":
        complaint.reporter_name = request.POST.get("reporter_name")
        complaint.phone_number = request.POST.get("phone_number")
        complaint.location = request.POST.get("location")
        complaint.road_name = request.POST.get("road_name")
        complaint.damage_type = request.POST.get("damage_type")
        complaint.severity = request.POST.get("severity")
        complaint.description = request.POST.get("description")
        complaint.status = request.POST.get("status")

        uploaded_photo = request.FILES.get("photo")
        if uploaded_photo:
            complaint.photo = uploaded_photo

        complaint.save()
        return redirect("complaint_list")

    return render(request, "main/complaint_form.html", {"complaint": complaint})


@login_required
@user_passes_test(lambda u: u.is_staff)
def complaint_delete(request, id):
    complaint = get_object_or_404(RoadDamageReport, id=id)
    complaint.delete()
    return redirect("complaint_list")
