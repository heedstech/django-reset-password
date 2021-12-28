from .base_email import BaseEmailMessage


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["code"] = context.get("code")
        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/password_changed_confirmation.html"


