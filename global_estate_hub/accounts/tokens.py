from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):
        return six.text_type(o=user.pk) + six.text_type(o=timestamp) + six.text_type(o=user.is_verified)


token_generator = TokenGenerator()
