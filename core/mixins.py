from django.contrib.auth.mixins import LoginRequiredMixin


class LoginCheckMixin(LoginRequiredMixin):
    login_url = "/"
    pass
