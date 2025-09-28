from django.contrib import admin
from .models import Word, GameSession
from django.db.models import Q

admin.site.register(Word)
admin.site.register(GameSession)

# Example function to get reports
def daily_report(date):
    sessions = GameSession.objects.filter(created_at__date=date)
    users_played = sessions.values('player').distinct().count()
    correct_guesses = sessions.filter(
        Q(guessed_words__contains=[{"status": "WIN"}])
    ).count()
    return {"users_played": users_played, "correct_guesses": correct_guesses}

def user_report(user_id):
    sessions = GameSession.objects.filter(player_id=user_id)
    total_words = sessions.count()
    correct = sum(1 for s in sessions if any(g["word"] == s.word.text for g in s.guessed_words))
    dates = sessions.values_list("created_at", flat=True)
    return {"total_words": total_words, "correct": correct, "dates": dates}
