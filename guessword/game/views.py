from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from .models import Word, GameSession

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "game/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "game/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    # Example dashboard
    if request.user.role == "ADMIN":
        return render(request, "game/admin_home.html")
    return render(request, "game/player_home.html")

@login_required
def start_game(request):
    # Limit 3 games per day
    today_sessions = GameSession.objects.filter(
        player=request.user,
        created_at__date=timezone.now().date()
    ).count()
    if today_sessions >= 3:
        return render(request, "game/limit.html", {"message": "Daily limit reached!"})

    word = Word.get_random_word()
    session = GameSession.objects.create(player=request.user, word=word)

    return redirect("make_guess", session_id=session.id)


@login_required
def make_guess(request, session_id):
    session = get_object_or_404(GameSession, id=session_id, player=request.user)

    if request.method == "POST":
        guess_word = request.POST.get("guess")
        result = session.make_guess(guess_word)

        # Redirect to game_over if game ended
        if result["status"] in ["WIN", "LOSE"]:
            return redirect("game_over", session_id=session.id)

        # Save invalid message in session
        if result["status"] == "INVALID":
            request.session['message'] = result["message"]

        # Redirect to GET after POST to prevent double submission
        return redirect("make_guess", session_id=session.id)

    # GET request
    message = request.session.pop('message', None)
    guesses_display = [list(zip(g["word"], g["feedback"])) for g in session.guessed_words]

    return render(request, "game/play.html", {
        "session": session,
        "guesses_display": guesses_display,
        "message": message
    })

@login_required
def game_over(request, session_id):
    session = get_object_or_404(GameSession, id=session_id, player=request.user)
    if session.guessed_words and session.guessed_words[-1]["word"] == session.word.text:
        result = "WIN"
    else:
        result = "LOSE"

    return render(request, "game/game_over.html", {
        "session": session,
        "result": result
    })

@login_required
def daily_report(request):
    if request.user.role != "ADMIN":
        return redirect("home")

    today = timezone.now().date()
    sessions_today = GameSession.objects.filter(created_at__date=today)

    users_played_count = sessions_today.values("player").distinct().count()

    # Precompute status for each session
    for s in sessions_today:
        if s.guessed_words and s.guessed_words[-1]["word"] == s.word.text:
            s.status = "WIN"
        else:
            s.status = "LOSE"

    # Count wins properly
    correct_guesses_count = sum(1 for s in sessions_today if s.status == "WIN")

    context = {
        "date": today,
        "users_played_count": users_played_count,
        "correct_guesses_count": correct_guesses_count,
        "sessions": sessions_today,
    }
    return render(request, "game/daily_report.html", context)


@login_required
def user_report(request):
    if request.user.role != "ADMIN":
        return redirect("home")

    users = User.objects.filter(role="PLAYER")
    report_data = []

    for user in users:
        sessions = GameSession.objects.filter(player=user)
        total_words = sessions.count()
        correct_words = sum(
            1 for s in sessions if s.guessed_words and s.guessed_words[-1]["word"] == s.word.text
        )
        dates_played = sessions.values_list("created_at__date", flat=True).distinct()
        report_data.append({
            "user": user,
            "dates_played": dates_played,
            "total_words": total_words,
            "correct_words": correct_words
        })

    return render(request, "game/user_report.html", {"report_data": report_data})