from django.contrib.auth.tokens import PasswordResetTokenGenerator
#from six import text_type
class TokenGenerator(PasswordResetTokenGenerator):
    pass
account_activation_token = TokenGenerator()