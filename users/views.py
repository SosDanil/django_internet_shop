import random
import secrets
import string

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http//{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейдите по ссылке, чтобы подтвердить почту: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    if request.method == 'GET':
        return render(request, 'users/reset.html')
    if request.method == 'POST':
        mail = request.POST.get('mail')
        user = get_object_or_404(User, email=mail)

        letters = list(string.ascii_lowercase)
        new_password = ''
        for _ in range(5):
            new_password = new_password + random.choice(letters) + str(random.randint(1, 9))

        user.set_password(new_password)
        user.save()

        message = (f"Ваш новый пароль: {new_password}\n"
                   f"Никому его не сообщайте")
        send_mail('Новый пароль', message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

        return redirect(reverse('users:login'))
