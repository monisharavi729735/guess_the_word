from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Extend User with roles (PLAYER / ADMIN)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PLAYER', 'Player'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLAYER')


# Store the words (initial 20 words will be seeded here)
class Word(models.Model):
    text = models.CharField(max_length=5, unique=True)  # always uppercase

    def __str__(self):
        return self.text


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
