from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import random
from django.core.exceptions import ValidationError


# Extend User with roles (PLAYER / ADMIN)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PLAYER', 'Player'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLAYER')

class Word(models.Model):
    text = models.CharField(max_length=5, unique=True)  # exactly 5 letters
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.text.upper()

    def clean(self):
        if len(self.text) != 5:
            raise ValidationError("Word must be exactly 5 letters.")

    def save(self, *args, **kwargs):
        self.text = self.text.upper()
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_random_word(cls):
        words = cls.objects.all()
        return random.choice(words) if words.exists() else None
    

# Game session for a player
class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_won = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # ends after win/loss

    def __str__(self):
        return f"Game {self.id} by {self.player.username}"


# Store each guess attempt
class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guesses")
    guess_text = models.CharField(max_length=5)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.guess_text} (Game {self.game.id})"


class GameSession(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    guessed_words = models.JSONField(default=list)  # store each guess as string
    attempts_left = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def make_guess(self, guess_word):
        guess_word = guess_word.upper()
        if not self.is_active:
            return {"status": "OVER", "message": "Game already ended"}

        if len(guess_word) != 5:
            return {"status": "INVALID", "message": "Guess must be 5 letters"}

        feedback = []
        target = list(self.word.text)
        guess = list(guess_word)

        # First pass for correct letters in correct positions (green)
        for i in range(5):
            if guess[i] == target[i]:
                feedback.append("GREEN")
                target[i] = None  # mark as used
            else:
                feedback.append(None)

        # Second pass for correct letters in wrong positions (orange)
        for i in range(5):
            if feedback[i] is None:
                if guess[i] in target:
                    feedback[i] = "ORANGE"
                    target[target.index(guess[i])] = None
                else:
                    feedback[i] = "GREY"

        self.guessed_words.append({"word": guess_word, "feedback": feedback})
        self.attempts_left -= 1

        # Check win/lose
        if guess_word == self.word.text:
            self.is_active = False
            status = "WIN"
        elif self.attempts_left <= 0:
            self.is_active = False
            status = "LOSE"
        else:
            status = "CONTINUE"

        self.save()
        return {"status": status, "feedback": feedback, "attempts_left": self.attempts_left}