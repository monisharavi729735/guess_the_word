from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("play/", views.start_game, name="start_game"),
    path("guess/<int:session_id>/", views.make_guess, name="make_guess"),
    path("game_over/<int:session_id>/", views.game_over, name="game_over"),
    path("reports/daily_report/", views.daily_report, name="daily_report"),
    path("reports/user_report/", views.user_report, name="user_report"),
]

