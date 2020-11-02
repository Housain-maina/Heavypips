from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import EmailMessage
from django.conf import settings
from twilio.rest import Client


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    paystack_customer_code = models.CharField(max_length=255)
    paystack_customer_subscription_code = models.CharField(max_length=255)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class About(models.Model):
    title = models.CharField(default='AboutPage', max_length=150)
    text = RichTextUploadingField(blank=True, null=True, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('signal-detail', kwargs={'pk': self.pk})


class Introduction(models.Model):
    title = models.CharField(default='IntroductionPage', max_length=150)
    text = RichTextUploadingField(blank=True, null=True, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Brokers(models.Model):
    name = models.CharField(default='Brokers Page', max_length=150)
    url = models.CharField(default='https://', max_length=1000)
    description = RichTextUploadingField(blank=True, null=True, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])

    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    body = RichTextUploadingField(blank=False, null=False, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.author}) ,{self.body}, {self.date_posted}'

class Signal(models.Model):
    pair = models.CharField(max_length=50)
    body = models.TextField(null=False, blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'({self.author}) ,{self.category}, {self.body}'

    def send(self, request):
        receiver = Customer.objects.filter(membership=True)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        for recepient in receiver:
            client.messages.create(to=recepient.phone, from_='Heavypips',
                                   body=f"{self.pair}, {self.body} ")


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signal-category-detail', kwargs={'slug': self.slug})


class Term(models.Model):
    title = models.CharField(default='TermsPage', max_length=150)
    text = RichTextUploadingField(blank=True, null=True, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Privacy(models.Model):
    title = models.CharField(default='PrivacyPage', max_length=150)
    text = RichTextUploadingField(blank=True, null=True, config_name='special', external_plugin_resources=[(
        'youtube',
        '/static/signalsection/vendor/ckeditor_plugins/youtube/youtube/',
        'plugin.js'
    )])
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Email(models.Model):
    email = models.EmailField(default='', max_length=255)

    def __str__(self):
        return self.email


class Number(models.Model):
    number = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.number


class Address(models.Model):
    address = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.address


class Social(models.Model):
    name = 'Social Media'
    instagram = models.CharField(max_length=255, null=True,blank=True)
    twitter = models.CharField(max_length=255, null=True,blank=True)
    facebook = models.CharField(max_length=255, null=True,blank=True)
    linkedin = models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField(null=True, blank=False, max_length=50, unique=True,
                              error_messages={'unique': 'This email is already registered in the database.'})
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email + "(" + str(self.confirmed) + ")"


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    content = models.FileField(upload_to='newsletter_uploads/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.subject} {self.created_at.strftime('%B %d, %Y')} by  {self.author}"

    def send(self, request):
        contents = self.content.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        for sub in subscribers:
            message = EmailMessage(
                from_email=settings.FROM_EMAIL,
                to=sub.emal,
                subject=self.subject,
                body=self.content + (
                    '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                    request.build_absolute_uri('/delete/'),
                    sub.email,
                    sub.conf_num))
            message.send()
