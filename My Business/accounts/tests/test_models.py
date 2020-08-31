import shutil
from django.test import TestCase
from django.conf import settings
from accounts.models import Account


class AccountsModelsTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_str(self):
        """Check __str__ correct"""
        self.assertEqual(self.user.__str__(), "Test User")
        self.assertEqual(self.superuser.__str__(), "Test Superuser")

    def test_get_full_name(self):
        """Check get_full_name correct"""
        self.assertEqual(self.user.get_full_name(), "Test User")
        self.assertEqual(self.superuser.get_full_name(), "Test Superuser")

    def test_is_superuser(self):
        """Check is_super_user correct"""
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.superuser.is_superuser, True)
