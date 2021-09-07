from django.test import TestCase

from accounts.models import Account


class AccountsManagersTestCase(TestCase):
    def test_create_user(self):
        """Check create_user successful"""
        Account.objects.create_user(email="email@example.com", password="normaluser")

    def test_create_user_email_incorrect(self):
        """Check create_user fail (no email)"""
        self.assertRaises(
            ValueError, Account.objects.create_user, email="", password="normaluser"
        )

    def test_create_superuser(self):
        """Check create_superuser successful"""
        Account.objects.create_superuser(
            email="email@example.com", password="superuser"
        )

    def test_create_superuser_is_incorrect(self):
        """Check create_superuser fail (no email)"""
        self.assertRaises(
            ValueError, Account.objects.create_superuser, email="", password="superuser"
        )

    def test_create_superuser_incorrect(self):
        """Check create_superuser fail (is_superuser=False)"""
        self.assertRaises(
            ValueError,
            Account.objects.create_superuser,
            email="email@example.com",
            password="superuser",
            is_superuser=False,
        )
