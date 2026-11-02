from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/approve/<int:user_id>/", views.approve_user, name="approve_user"),
    path("analytics/", views.analytics, name="analytics"),
    path("report/", views.report, name="report"),
    path("complaints/", views.complaint_list, name="complaint_list"),
    path("complaints/create/", views.complaint_create, name="complaint_create"),
    path("complaints/<int:id>/update/", views.complaint_update, name="complaint_update"),
    path("complaints/<int:id>/delete/", views.complaint_delete, name="complaint_delete"),
]
