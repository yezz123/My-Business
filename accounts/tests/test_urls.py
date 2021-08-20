from django.test import TestCase
from django.urls import resolve


class AccountsUrlsCase(TestCase):
    def test_login(self):
        """Check login URL correct"""
        self.assertEqual(resolve("/accounts/login/").view_name, "accounts:login")

    def test_logout(self):
        """Check logout URL correct"""
        self.assertEqual(resolve("/accounts/logout/").view_name, "accounts:logout")

    def test_passoword_reset(self):
        """Check password reset URL correct"""
        self.assertEqual(
            resolve("/accounts/password/reset/").view_name, "accounts:password_reset"
        )

    def test_password_reset_confirm(self):
        """Check password reset confirm URL correct"""
        self.assertEqual(
            resolve("/accounts/password/reset/-1/-1/").view_name,
            "accounts:password_reset",
        )

    def test_password_change(self):
        """Check password change URL correct"""
        self.assertEqual(
            resolve("/accounts/999999/password/change/").view_name,
            "accounts:password_change",
        )

    def test_list(self):
        """Check password change URL correct"""
        self.assertEqual(resolve("/accounts/").view_name, "accounts:list")

    def test_detail(self):
        """Check password change URL correct"""
        self.assertEqual(resolve("/accounts/999999/").view_name, "accounts:detail")

    def test_edit(self):
        """Check password change URL correct"""
        self.assertEqual(resolve("/accounts/999999/edit/").view_name, "accounts:edit")

    def test_delete(self):
        """Check password change URL correct"""
        self.assertEqual(
            resolve("/accounts/999999/delete/").view_name, "accounts:delete"
        )
