from django.test import TestCase
from accounts.apps import AccountsConfig


class AccountsAppsTestCase(TestCase):
    def test_name(self):
        """Check name correct"""
        self.assertEqual(AccountsConfig.name, "accounts")
