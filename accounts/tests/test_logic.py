from django.contrib.auth.tokens import default_token_generator as token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Account


class AccountsLoginTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check login template"""
        response = self.client.get("/accounts/login/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/login.html")

    def test_successful(self):
        """Check login successful"""
        response = self.client.post(
            "/accounts/login/",
            {"email": self.user.email, "password": "test_user123"},
            follow=True,
        )
        self.assertContains(
            response,
            f"Welcome back, {self.user.first_name}! You have successfully logged in.",
        )
        self.client.logout()
        response = self.client.post(
            "/accounts/login/",
            {"email": self.superuser.email, "password": "test_superuser123"},
            follow=True,
        )
        self.assertContains(
            response,
            f"Welcome back, {self.superuser.first_name}! You have successfully logged in.",
        )

    def test_incorrect_active(self):
        """Check login unsuccessful (is_active)"""
        self.user.is_active = False
        self.superuser.is_active = False
        self.user.save()
        self.superuser.save()
        response = self.client.post(
            "/accounts/login/",
            {"email": self.user.email, "password": "test_user123"},
            follow=True,
        )
        self.assertContains(response, "Your account has not been activated.")
        response = self.client.post(
            "/accounts/login/",
            {"email": self.superuser.email, "password": "test_superuser123"},
            follow=True,
        )
        self.assertContains(response, "Your account has not been activated.")

    def test_incorrect_email(self):
        """Check login unsuccessful (email)"""
        response = self.client.post(
            "/accounts/login/",
            {"email": self.user.email + "1", "password": "test_user123"},
            follow=True,
        )
        self.assertContains(
            response, "The email and/or password you entered are incorrect."
        )
        response = self.client.post(
            "/accounts/login/",
            {"email": self.superuser.email + "1", "password": "test_superuser123"},
            follow=True,
        )
        self.assertContains(
            response, "The email and/or password you entered are incorrect."
        )
        response = self.client.post(
            "/accounts/login/",
            {"email": "", "password": "test_superuser123"},
            follow=True,
        )
        self.assertContains(response, "This field is required.")

    def test_incorrect_password(self):
        """Check login unsuccessful (password)"""
        response = self.client.post(
            "/accounts/login/",
            {"email": self.user.email, "password": "test_user12345"},
            follow=True,
        )
        self.assertContains(
            response, "The email and/or password you entered are incorrect."
        )
        response = self.client.post(
            "/accounts/login/", {"email": self.user.email, "password": ""}, follow=True,
        )
        self.assertContains(response, "This field is required.")
        response = self.client.post(
            "/accounts/login/",
            {"email": self.superuser.email, "password": "test_superuser12345"},
            follow=True,
        )
        self.assertContains(
            response, "The email and/or password you entered are incorrect."
        )
        response = self.client.post(
            "/accounts/login/",
            {"email": self.superuser.email, "password": ""},
            follow=True,
        )
        self.assertContains(response, "This field is required.")

    def test_already_logged_in(self):
        """Check login unsuccessful (logged in)"""
        self.client.force_login(self.user)
        response = self.client.get("/accounts/login/", follow=True)
        self.assertContains(response, "You are already logged in!")
        self.client.force_login(self.superuser)
        response = self.client.get("/accounts/login/", follow=True)


class AccountsLogoutTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_successful(self):
        """Check logout successful"""
        self.client.force_login(self.user)
        response = self.client.get("/accounts/logout/", follow=True)
        self.assertContains(response, "You have successfully logged out.")
        self.client.force_login(self.superuser)
        response = self.client.get("/accounts/logout/", follow=True)
        self.assertContains(response, "You have successfully logged out.")

    def test_warning(self):
        """Check logout successful (warning)"""
        response = self.client.get("/accounts/logout/", follow=True)
        self.assertContains(response, "You are already logged out!")


class AccountsPasswordResetTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check password reset template"""
        response = self.client.get("/accounts/password/reset/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/password/reset.html")

    def test_successful(self):
        """Check password reset successful"""
        response = self.client.post(
            "/accounts/password/reset/", {"email": self.user.email}, follow=True
        )
        self.assertContains(
            response, "You have successfully requested a password reset."
        )
        response = self.client.post(
            "/accounts/password/reset/", {"email": self.superuser.email}, follow=True
        )
        self.assertContains(
            response, "You have successfully requested a password reset."
        )

    def test_redirect(self):
        """Check password reset redirect"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/password/reset/", follow=True)
        self.assertContains(
            response,
            "You have been redirected to change your password because you are logged in!",
        )
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/password/reset/", follow=True)
        self.assertContains(
            response,
            "You have been redirected to change your password because you are logged in!",
        )

    def test_incorrect_email(self):
        """Check password reset unsuccessful (email)"""
        response = self.client.post(
            "/accounts/password/reset/", {"email": ""}, follow=True
        )
        self.assertContains(response, "This field is required.")
        response = self.client.post(
            "/accounts/password/reset/",
            {"email": "stefan.business@example.com"},
            follow=True,
        )
        self.assertContains(
            response, "The email is not associated with any active accounts."
        )


class AccountsPasswordResetConfirmTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check password reset confirm template"""
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            follow=True,
        )
        self.assertTemplateUsed(response, template_name="accounts/password/reset.html")

    def test_valid(self):
        """Check password reset confirm valid"""
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            follow=True,
        )
        self.assertContains(response, "Verify New Password")
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.superuser.uid))}/{token_generator.make_token(self.superuser)}/",
            follow=True,
        )
        self.assertContains(response, "Verify New Password")

    def test_successful(self):
        """Check password reset confirm successful"""
        response = self.client.post(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password123",
            },
            follow=True,
        )
        self.assertContains(response, "You have successfully reset your password.")
        self.client.login(email=self.user.email, password="test_password123")
        self.client.logout()
        response = self.client.post(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.superuser.uid))}/{token_generator.make_token(self.superuser)}/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password123",
            },
            follow=True,
        )
        self.assertContains(response, "You have successfully reset your password.")
        self.client.login(email=self.superuser.email, password="test_password123")

    def test_redirect(self):
        """Check password reset confirm redirect"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            follow=True,
        )
        self.assertContains(
            response,
            "You have been redirected to change your password because you are logged in!",
        )
        self.client.force_login(self.superuser)
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.superuser.uid))}/{token_generator.make_token(self.superuser)}/",
            follow=True,
        )
        self.assertContains(
            response,
            "You have been redirected to change your password because you are logged in!",
        )

    def test_incorrect_password(self):
        """Check password reset confirm unsuccessful (incorrect)"""
        response = self.client.post(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password",
            },
            follow=True,
        )
        self.assertContains(response, "The passwords do not match.")
        response = self.client.post(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            {"new_password": "", "verify_new_password": ""},
            follow=True,
        )
        self.assertContains(response, "This field is required.")
        response = self.client.post(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/{token_generator.make_token(self.user)}/",
            {"new_password": "test_password", "verify_new_password": "test_password"},
            follow=True,
        )
        self.assertContains(
            response,
            "The password needs to have at least 8 characters, a letter, and a number.",
        )

    def test_incorrect_token(self):
        """Check password reset confirm unsuccessful (token)"""
        response = self.client.get(
            f"/accounts/password/reset/MA245/{token_generator.make_token(self.user)}/",
            follow=True,
        )
        self.assertContains(response, "The request is invalid.")
        response = self.client.get(
            f"/accounts/password/reset/{urlsafe_base64_encode(force_bytes(self.user.uid))}/123412/",
            follow=True,
        )
        self.assertContains(response, "The request is invalid.")


class AccountsPasswordChangeTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check password change template"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"/accounts/{self.user.uid}/password/change/", follow=True
        )
        self.assertTemplateUsed(response, template_name="accounts/password/change.html")

    def test_successful(self):
        """Check password change successful"""
        self.client.force_login(self.user)
        response = self.client.post(
            f"/accounts/{self.user.uid}/password/change/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password123",
            },
            follow=True,
        )
        self.assertContains(response, "You have successfully changed your password.")
        self.client.login(email=self.user.email, password="test_password123")
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.superuser.uid}/password/change/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password123",
            },
            follow=True,
        )
        self.assertContains(response, "You have successfully changed your password.")
        self.client.login(email=self.superuser.email, password="test_password123")

    def test_incorrect_permissions(self):
        """Check password change unsuccessful (permissions)"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"/accounts/{self.user.uid}/password/change/", follow=True
        )
        self.assertContains(response, "Verify New Password")
        response = self.client.get(
            f"/accounts/{self.superuser.uid}/password/change/", follow=True
        )
        self.assertContains(response, "You don&#39;t have the required permissions.")

        self.client.force_login(self.superuser)
        response = self.client.get(
            f"/accounts/{self.user.uid}/password/change/", follow=True
        )
        self.assertContains(response, "Verify New Password")
        response = self.client.get(
            f"/accounts/{self.superuser.uid}/password/change/", follow=True
        )
        self.assertContains(response, "Verify New Password")

    def test_incorrect_password(self):
        """Check password change unsuccessful (incorrect)"""
        self.client.force_login(self.user)
        response = self.client.post(
            f"/accounts/{self.user.uid}/password/change/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password12345",
            },
            follow=True,
        )
        self.assertContains(response, "The passwords do not match.")
        response = self.client.post(
            f"/accounts/{self.user.uid}/password/change/",
            {"new_password": "", "verify_new_password": ""},
            follow=True,
        )
        self.assertContains(response, "This field is required.")
        response = self.client.post(
            f"/accounts/{self.user.uid}/password/change/",
            {"new_password": "test_password", "verify_new_password": "test_password"},
            follow=True,
        )
        self.assertContains(
            response,
            "The password needs to have at least 8 characters, a letter, and a number.",
        )
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.superuser.uid}/password/change/",
            {
                "new_password": "test_password123",
                "verify_new_password": "test_password12345",
            },
            follow=True,
        )
        self.assertContains(response, "The passwords do not match.")
        response = self.client.post(
            f"/accounts/{self.superuser.uid}/password/change/",
            {"new_password": "", "verify_new_password": ""},
            follow=True,
        )
        self.assertContains(response, "This field is required.")
        response = self.client.post(
            f"/accounts/{self.superuser.uid}/password/change/",
            {"new_password": "test_password", "verify_new_password": "test_password"},
            follow=True,
        )
        self.assertContains(
            response,
            "The password needs to have at least 8 characters, a letter, and a number.",
        )

    def test_incorrect_account(self):
        """Check password change unsuccessful (account)"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/999999/password/change/", follow=True)
        self.assertContains(response, "The account doesn&#39;t exist.")


class AccountsListTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check list template"""
        self.client.force_login(self.superuser)
        response = self.client.get("/accounts/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/list.html")

    def test_successful(self):
        """Check list successful"""
        self.client.force_login(self.superuser)
        response = self.client.get("/accounts/", follow=True)
        self.assertContains(response, self.user.uid)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.superuser.uid)
        self.assertContains(response, self.superuser.first_name)
        self.assertContains(response, self.superuser.last_name)
        self.assertContains(response, self.superuser.email)

    def test_incorrect_permissions(self):
        """Check list unsuccessful (permissions)"""
        self.client.force_login(self.user)
        response = self.client.get("/accounts/", follow=True)
        self.assertContains(response, "You don&#39;t have the required permissions.")


class AccountsDetailTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check detail template"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/detail.html")

    def test_successful(self):
        """Check detail successful"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/{self.user.uid}/", follow=True)
        self.assertContains(response, self.user.uid)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.company)
        self.assertContains(response, self.user.address1)
        self.assertContains(response, self.user.country.name)
        response = self.client.get(f"/accounts/{self.superuser.uid}/", follow=True)
        self.assertContains(response, self.superuser.uid)
        self.assertContains(response, self.superuser.first_name)
        self.assertContains(response, self.superuser.last_name)
        self.assertContains(response, self.superuser.email)

    def test_incorrect_permissions(self):
        """Check detail unsuccessful (permissions)"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/", follow=True)
        self.assertContains(response, self.user.get_full_name())
        response = self.client.get(f"/accounts/{self.superuser.uid}/", follow=True)
        self.assertContains(response, "You don&#39;t have the required permissions.")
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/{self.superuser.uid}/", follow=True)
        self.assertContains(response, self.superuser.get_full_name())
        response = self.client.get(f"/accounts/{self.user.uid}/", follow=True)
        self.assertContains(response, self.user.get_full_name())

    def test_incorrect_account(self):
        """Check detail unsuccessful (account)"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/999999/", follow=True)
        self.assertContains(response, "The account doesn&#39;t exist.")


class AccountsEditTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check edit template"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/edit/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/edit.html")

    def test_date(self):
        """Check edit data"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/{self.user.uid}/edit/", follow=True)
        self.assertContains(response, self.user.uid)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.company)
        self.assertContains(response, self.user.address1)
        self.assertContains(response, self.user.country.code)
        response = self.client.get(f"/accounts/{self.superuser.uid}/edit/", follow=True)
        self.assertContains(response, self.superuser.uid)
        self.assertContains(response, self.superuser.first_name)
        self.assertContains(response, self.superuser.last_name)
        self.assertContains(response, self.superuser.email)

    def test_successful(self):
        """Check edit successful"""
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "uid": self.user.uid,
                "email": self.user.email,
                "verify_email": self.user.email,
                "first_name": "John",
                "last_name": "Smith",
                "date_of_birth": "2000-01-01",
            },
            follow=True,
        )
        self.assertContains(response, "The account has been successfully edited.")
        response = self.client.post(
            f"/accounts/{self.superuser.uid}/edit/",
            {
                "uid": self.superuser.uid,
                "email": "John.business@example.com",
                "verify_email": "John.business@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "avatar": self.user.avatar_url,
            },
            follow=True,
        )
        self.assertContains(response, "The account has been successfully edited.")

    def test_incorrect_permissions(self):
        """Check edit unsuccessful (permissions)"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/edit/", follow=True)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        response = self.client.get(f"/accounts/{self.superuser.uid}/edit/", follow=True)
        self.assertContains(response, "You don&#39;t have the required permissions.")
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/{self.superuser.uid}/edit/", follow=True)
        self.assertContains(response, self.superuser.first_name)
        self.assertContains(response, self.superuser.last_name)
        response = self.client.get(f"/accounts/{self.user.uid}/edit/", follow=True)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_incorrect_email(self):
        """Check edit unsuccessful (email)"""
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "email": self.user.email,
                "verify_email": self.user.email + "1",
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
            follow=True,
        )
        self.assertContains(response, "The emails do not match.")
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "uid": self.user.uid,
                "email": "",
                "verify_email": "",
                "last_name": self.user.first_name,
                "first_name": self.user.last_name,
            },
            follow=True,
        )
        self.assertContains(response, "This field is required.")

    def test_incorrect_first_name(self):
        """Check edit unsuccessful (first name)"""
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "email": self.user.email,
                "verify_email": self.user.email,
                "first_name": "!^$&#(1234",
                "last_name": self.user.last_name,
            },
            follow=True,
        )
        self.assertContains(response, "Enter a valid first name.")

    def test_incorrect_last_name(self):
        """Check edit unsuccessful (last name)"""
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "email": self.user.email,
                "verify_email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": "!^$&#(1234",
            },
            follow=True,
        )
        self.assertContains(response, "Enter a valid last name.")

    def test_incorrect_date_of_birth(self):
        """Check edit unsuccessful (date of birth)"""
        self.client.force_login(self.superuser)
        response = self.client.post(
            f"/accounts/{self.user.uid}/edit/",
            {
                "email": self.user.email,
                "verify_email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "date_of_birth": "3000-01-01",
            },
            follow=True,
        )
        self.assertContains(response, "The date of birth cannot be in the future.")

    def test_incorrect_account(self):
        """Check edit unsuccessful (account)"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/999999/edit/", follow=True)
        self.assertContains(response, "The account doesn&#39;t exist.")


class AccountsDeleteTestCase(TestCase):
    fixtures = ["tests/test_data/accounts.json", "core/fixtures/initial_data.json"]

    def setUp(self):
        """Set up accounts"""
        self.user = Account.objects.get(is_superuser=False)
        self.superuser = Account.objects.get(is_superuser=True)

    def test_template(self):
        """Check delete template"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/delete/", follow=True)
        self.assertTemplateUsed(response, template_name="accounts/delete.html")

    def test_successful(self):
        """Check delete successful"""
        self.client.force_login(self.superuser)
        response = self.client.post(f"/accounts/{self.user.uid}/delete/", follow=True)
        self.assertContains(response, "The account has been deleted.")

    def test_permissions_non_superuser(self):
        """Check delete unsuccessful (permissions)"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/{self.user.uid}/delete/", follow=True)
        self.assertContains(response, "Delete")
        response = self.client.get(
            f"/accounts/{self.superuser.uid}/delete/", follow=True
        )
        self.assertContains(response, "You don&#39;t have the required permissions.")
        self.client.force_login(self.superuser)
        response = self.client.get(
            f"/accounts/{self.superuser.uid}/delete/", follow=True
        )
        self.assertContains(response, "Delete")
        response = self.client.get(f"/accounts/{self.user.uid}/delete/", follow=True)
        self.assertContains(response, "Delete")

    def test_incorrect_account(self):
        """Check delete unsuccessful (account)"""
        self.client.force_login(self.superuser)
        response = self.client.get(f"/accounts/999999/delete/", follow=True)
        self.assertContains(response, "The account doesn&#39;t exist.")
