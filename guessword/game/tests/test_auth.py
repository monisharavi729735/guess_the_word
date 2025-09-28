from django.test import TestCase
from django.urls import reverse

class AuthTests(TestCase):
    def test_username_validation(self):
        # too short
        response = self.client.post(reverse("register"), {
            "username": "abc",
            "password1": "Test1@",
            "password2": "Test1@",
            "role": "PLAYER"
        })
        self.assertContains(response, "Username must be at least 5 characters long.")

        # no uppercase
        response = self.client.post(reverse("register"), {
            "username": "monisha",
            "password1": "Test1@",
            "password2": "Test1@",
            "role": "PLAYER"
        })
        self.assertContains(response, "Username must include both uppercase and lowercase letters.")

    def test_password_validation(self):
        # no special char
        response = self.client.post(reverse("register"), {
            "username": "Monisha",
            "password1": "abc12",
            "password2": "abc12",
            "role": "PLAYER"
        })
        self.assertContains(response, "Password must contain at least one special char")

    def test_successful_registration_and_login(self):
        response = self.client.post(reverse("register"), {
            "username": "Monisha",
            "password1": "HelloWorld123@",
            "password2": "HelloWorld123@",
            "role": "PLAYER"
        })
        self.assertRedirects(response, reverse("home"))  # auto-login works

        # logout and login back
        self.client.get(reverse("logout"))
        login = self.client.post(reverse("login"), {"username": "Monisha", "password": "HelloWorld123@"})
        self.assertRedirects(login, reverse("home"))
