from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ContactForm, SubscriberForm, UserUpdaetForm
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser
from signalsection.models import Email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .tokens import AccountActivationTokenGenerator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model


def register(request):
    # if request.method == 'GET':
    #     return render(request, 'users/register.html')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, f'Your Account has been created and an Activation link has been sent to your email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account Activation'
            message = render_to_string('users/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_link = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            send_link.send()
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Your Account has been activated you can now login')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid')


def ContactView(request):
    name = ''
    user_email = ''
    comment = ''

    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        user_email = form.cleaned_data.get('user_email')
        comment = form.cleaned_data.get('comment')
        subject = "Heavypips Contact Form Feedback"

        comment = name + " with email address " + user_email + " says:\n " + comment
        send_mail(subject=subject, from_email=user_email, message=comment,
                  recipient_list=['hussainmaina27@gmail.com'])

        context = {'form': form, 'title': 'Contact Us'}
        return render(request, 'users/contact.html', context)

    else:
        context = {'form': form, 'title': 'Contact Us'}
        return render(request, 'users/contact.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdaetForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Account Has Been Updated!')
            return redirect('settings')
    else:
        form = UserUpdaetForm(instance=request.user)
    context = {'form': form, 'title': 'Settings'}
    return render(request, 'users/settings.html', context)

