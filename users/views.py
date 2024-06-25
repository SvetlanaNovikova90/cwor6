from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm, VerificationCodeForm

from users.models import User
from django.contrib.auth import login

from django.urls import reverse_lazy
from django.views import View

from utils import generate_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        # Пользователь не активен до верификации
        new_user.is_active = False
        # получение кода для почты
        verification_code = generate_password()
        # сохранение кода в поле юзера
        new_user.verification_code = verification_code
        new_user.save()

        # Отправка кода верификации на почту
        send_mail(
            subject='Проверка почты',
            message=f'Ваш код верификации: {verification_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        # Перенаправление пользователя на страницу ввода кода верификации
        return redirect('users:verify_email', pk=new_user.pk)


class VerifyEmailView(View):
    """
    Верификация почты
    """
    template_name = 'users/verify_email.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = VerificationCodeForm()
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = VerificationCodeForm(request.POST)
        # проверка кода
        if form.is_valid() and user.verification_code == form.cleaned_data['verification_code']:
            # юзер становится активным
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_activated')
        return render(request, self.template_name, {'form': form, 'user': user})


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('main:main')

    def get_object(self, queryset=None):
        return self.request.user


def email_activate(request):
    """
    Контроллер для страницы, которая выводит информацию юзеру об успешности
    верификации почты
    """
    return render(request, "users/email_activate.html")


def activate(request, uid):
    """
    Контроллер для активации пользователя при восстановлении пароля
    """
    user = User.objects.filter(email_verify=int(uid)).first()
    user.is_active = True
    user.save()
    return redirect(reverse('main:main'))


def restore_password(request):
    """
    Контроллер для верификации пароля
    """
    if request.method == "POST":
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        new_password = generate_password()
        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, "users/restore_password.html")

