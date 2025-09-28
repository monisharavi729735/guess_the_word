from django.test import TestCase
from django.contrib.auth import get_user_model
from game.models import Word, GameSession

User = get_user_model()

class GameTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player1", password="Test123@")
        self.word = Word.objects.create(text="APPLE")

    def test_start_game(self):
        session = GameSession.objects.create(player=self.user, word=self.word)
        self.assertEqual(session.attempts_left, 5)
        self.assertEqual(session.guessed_words, [])

    def test_correct_guess(self):
        session = GameSession.objects.create(player=self.user, word=self.word)
        res = session.make_guess("APPLE")
        self.assertEqual(res["status"], "WIN")
        self.assertFalse(session.is_active)

    def test_incorrect_guess(self):
        session = GameSession.objects.create(player=self.user, word=self.word)
        res = session.make_guess("BERRY")
        self.assertEqual(res["status"], "CONTINUE")
        self.assertEqual(session.attempts_left, 4)
