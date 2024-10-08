from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user,timestamp):
        return (
           print(text_type(user.pk)+text_type(timestamp)+text_type(user.is_active))
        )

account_activation_token = AccountActivationTokenGenerator()