from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    """View for login"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Bookshelf - Authorization'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    """View for registration"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Congratulations! You have successfully registered.'
    title = 'Bookshelf - Registration'


class UserProfileView(TitleMixin, UpdateView):
    """View for personal account"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Bookshelf - Personal Area'

    def get_success_url(self):
        """After saving the profile data, leave the user in the profile"""
        return reverse_lazy('users:profile', args=(self.object.id,))
        # We do not use success_url, because the personal account (UpdateView) is linked to the user
        # and has the path users/profile/<int:pk>/. We have to insert the user id into the path.


class EmailVerificationView(TitleMixin, TemplateView):
    """View with email confirmation"""
    title = 'Bookshelf - Email confirmation'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        """Compare the resulting code with what is in the database"""
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # If use get() and the object does not exist, then there will be an error.
        # If use filter() and the object does not exist, an empty list will be returned.
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


