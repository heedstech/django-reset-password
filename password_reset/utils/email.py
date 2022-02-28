from .base_email import BaseEmailMessage


class PasswordResetEmail(BaseEmailMessage):
    template_name = "password_reset/email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["code"] = context.get("code")
        context["email"] = context.get("email")
        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "password_reset/email/password_changed_confirmation.html"


