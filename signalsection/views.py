from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import About, Introduction, Term, Privacy, Signal, Customer, Brokers, Subscriber, Newsletter, Announcement
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from celery.schedules import crontab
from django.contrib import messages
from celery.task import periodic_task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, AccessMixin
from paystackapi.paystack import Paystack
from django.utils.decorators import method_decorator
from django_twilio.decorators import twilio_view
from users.forms import SubscriberForm
from django.conf import settings
from twilio.rest import Client
import random
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from signalsection.models import Subscriber
from users.decorators import signal_required, newsletter_required
from users.forms import SubscriberForm, NewsletterForm
from django.contrib.auth import get_user_model
import uuid
import datetime
pstk_key = settings.PAYSTACK_KEY
pstk = Paystack(secret_key=pstk_key)


@periodic_task(run_every=crontab(minute=0))
def updateaccount(request):
    customer_status = Customer.objects
    for customer in customer_status:
        subscription = pstk.subscription.fetch(customer.paystack_customer_subscription_code)
        if subscription['data']['status'] == 'active':
            customer.membership = True
            customer.save()
        else:
            customer.membership = False
            customer.save()
    return HttpResponse('completed')


def randoms_digits():
    return "0.12d" % random.randint(0, 999999999999)


def random_digits():
    password = uuid.uuid4()
    return password


@csrf_exempt
def home(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        sub = Subscriber()
        email = form.cleaned_data.get('email')
        try:
            filterss = Subscriber.objects.get(email =email)
        except Subscriber.DoesNotExist:
            filterss = None
        if filterss == None:
            sub.email = form.cleaned_data.get('email')
            sub.conf_num = random_digits()
            sub.save()
            message = EmailMessage(
                from_email='noreply@heavypips.com',
                to=[form.cleaned_data.get('email')],
                subject='Newsletter Confirmation',
                body='Thank you for signing up for our email newsletter! \
                                  Please complete the process by \
                                  <a href="{}?email={}&conf_num={}"> \
                                  clicking here to confirm your registration</a>'.format(
                    request.build_absolute_uri('/confirm/'),
                    sub.email,
                    sub.conf_num))
            message.send()

            return HttpResponse('An Activation link has been sent to your email with instructions.', 200)
        else:
            return HttpResponse('This email is already registeredin the database, please use a different one.', 404)
    else:
        return render(request, 'signalsection/home.html', {'form': form, 'title': 'Home'})


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return HttpResponse('You have successfully subscribe to our newsletter')
    else:
        return HttpResponse('Invalid Confirmation Details')


def delete(request):
    try:
        filterss = Subscriber.objects.get(email=request.GET['email'])
    except Subscriber.DoesNotExist:
        filterss = None
    if filterss:
        if filterss.conf_num == request.GET['conf_num']:
            filterss.delete()
            return HttpResponse('You have successfully unsubscribed.')
        else:
            return HttpResponse('Invalid details.')
    else:
        return HttpResponse('Subscriber does not exist')


@newsletter_required
def newsletter(request):
    form = NewsletterForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data.get('subject')
        content = form.cleaned_data.get('content').read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        newsletters = Newsletter(subject=subject, content=content)
        newsletters.save()
        messages.success(request, f'Newsletter has been sent!')
        for sub in subscribers:
            message = EmailMessage(
                from_email='hussainmaina27@gmail.com',
                to=[sub.email],
                subject=subject,
                body=content + (
                    '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                    request.build_absolute_uri('/delete/'),
                    sub.email,
                    sub.conf_num))
            message.send()
        return render(request, 'signalsection/newsletter.html', {'title': 'Newsletter', 'form': form})
    else:
        return render(request, 'signalsection/newsletter.html', {'title': 'Newsletter', 'form': form})


def about(request):
    about = About.objects.all
    return render(request, 'signalsection/about.html', {'title': 'About', 'about': about,})


def brokers(request):
    brokers = Brokers.objects.all
    return render(request, 'signalsection/brokers.html', {'title': 'Brokers', 'brokers': brokers})


def introduction(request):
    introduction = Introduction.objects.all
    return render(request, 'signalsection/introduction.html', {'title': 'Introduction', 'intro': introduction})


def charts(request):
    return render(request, 'signalsection/charts.html', {'title': 'Charts'})


def terms(request):
    terms = Term.objects.all
    return render(request, 'signalsection/terms.html', {'terms': terms, 'title': 'Terms of Use'})


def privacy(request):
    privacy = Privacy.objects.all
    return render(request, 'signalsection/privacy.html', {'privacy': privacy, 'title': 'Privacy Policy'})


def subscribe(request):
    return render(request, 'signalsection/subscribe.html', {'title': 'Subscribe'})


def signalsub(request):
    return render(request, 'signalsection/signalsub.html', {'title': 'Signals'})


@login_required
def checkout(request):
    try:
        if request.user.customer.membership:
            return redirect('dashboard')
    except Customer.DoesNotExist:
        pass
    if request.method == 'POST':
        pstk_user = pstk.customer.create(email=request.user.email,
                                         first_name=request.user.first_name,
                                         last_name=request.user.last_name,
                                         phone= str(request.user.phone),
                                         )
        plan_code = 'PLN_6f1b0f6pssxrill'
        if request.POST.get('plan') == 'signalyearly':
            plan_code = 'PLN_yfxeiya576eivzz'

        else:
            customer_subscription = pstk.subscription.create(customer=pstk_user['data']['customer_code'],
                                                             plan=plan_code)
            customer = Customer()
            customer.user = request.user
            customer.paystack_customer_code = pstk_user['data']['customer_code']
            customer.phone = request.user.phone
            customer_code = pstk_user['data']['customer_code']
            customer.membership = True
            subscription_code = pstk.customer.get(customer_code)
            customer.paystack_customer_subscription_code = subscription_code['data']['subscriptions'][0]['subscription_code']
            customer.save()
            return redirect('dashboard')
    else:
        plan = 'signalmonthly'
        name = 'Monthly Signal'
        price = 5000
        plan_code = 'PLN_6f1b0f6pssxrill'
        title_plan = 'Monthly Plan'
        if request.method == 'GET':
            if request.GET['plan'] == 'signalyearly':
                plan = 'signalyearly'
                price = 50000
                name = 'Yearly Signals'
                plan_code = 'PLN_yfxeiya576eivzz'
                title_plan = 'Yearly Plan'

        return render(request, 'signalsection/checkout.html',
                      {'plan_code': plan_code, 'price': price, 'title': f'{ title_plan }', 'name': name, })


class MembershipUpdateMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        customers = Customer.objects.all
        for customer in customers:
            subscription = pstk.subscription.fetch(customer.paystack_customer_subscription_code)
            if subscription['data']['status'] == 'active':
                customer.membership = True
                customer.save()
                return redirect('dashboard')
            else:
                customer.membership = False
                customer.save()
                return redirect('checkout')
        return super(MembershipUpdateMixin, self).dispatch(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, ListView):
    model = Signal
    template_name = 'signalsection/dashboard.html'
    context_object_name = 'signals'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Dashboard'
        today = datetime.datetime.now()
        last3 = datetime.timedelta(days=2)
        finaldays = today - last3
        announcement = Announcement.objects.filter(date_posted__gte=finaldays).order_by('-date_posted')
        context['announcement'] = announcement
        context['title'] = title
        return context


class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)


@method_decorator([signal_required], name='dispatch')
class SignalCreateView(UserPassesTestMixin, CreateView):
    model = Signal
    fields = ['category', 'pair', 'body']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'signal created with success!')
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_signalmanager:
            return True
        return False

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            for customer in Customer.objects.all():
                subscription = pstk.subscription.fetch(customer.paystack_customer_subscription_code)
                if subscription['data']['status'] == 'active':
                    customer.membership = True
                    customer.save()
                else:
                    customer.membership = False
                    customer.save()
            receiver = Customer.objects.filter(membership=True)
            access = get_user_model().filter(allowaccess=True)
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            for recepient in receiver:
                client.messages.create(to=recepient.phone, from_='Heavypips',
                                        body=f"{request.POST.get('pair')}:\n {request.POST.get('body')} \n Happy Trading")
            for user in access:
                client.messages.create(to=user.phone, from_='Heavypips',
                                       body=f"{request.POST.get('pair')}:\n {request.POST.get('body')}")
                messages.success(request, f'signal sent successfully')
                return redirect()
        return super().dispatch(request, *args, **kwargs)


@method_decorator([signal_required], name='dispatch')
class SignalUpdateView(UserPassesTestMixin, UpdateView):
    model = Signal
    fields = ['category', 'pair', 'body']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'signal updated with success!')
        return super().form_valid(form)

    def test_func(self):
        signal = self.get_object()
        if self.request.user == signal.author or self.request.user.is_staff:
            return True
        return False


@method_decorator([signal_required], name='dispatch')
class SignalDeleteView(UserPassesTestMixin, DeleteView):
    model = Signal
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.ERROR(self.request, 'signal deleted with success!')
        return super().form_valid(form)

    def test_func(self):
        signal = self.get_object()

        if self.request.user == signal.author or self.request.user.is_staff:
            return True
        return False


@method_decorator([signal_required], name='dispatch')
class AnnouncementCreateView(UserPassesTestMixin, CreateView):
    model = Announcement
    fields = ['body']
    template_name = 'signalsection/announcement_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Added Announcement!')
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_signalmanager:
            return True
        return False


@method_decorator([signal_required], name='dispatch')
class UserSignalsListView(ListView):
    model = Signal
    template_name = 'signalsection/user_signals.html'
    context_object_name = 'signals'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), email=self.kwargs.get('email'))
        return Signal.objects.filter(author=user).order_by('-date_posted')
