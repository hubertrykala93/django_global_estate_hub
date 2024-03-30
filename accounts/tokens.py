from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Creating TokenGenerator.
    """

    def _make_hash_value(self, user, timestamp) -> str:
        """
        Generates a token for the user for the purpose of account activation.

        Parameters
        ----------
            user: account.models.User
            timestamp: int

        Returns
        ----------
            str
        """
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_verified)


token_generator = TokenGenerator()
