from django.contrib import admin
from .models import Signal, Category, About, Introduction, Announcement, Term, Customer, Brokers, Social, Email, Address, Number, Subscriber, Newsletter


admin.site.register(Signal)
admin.site.register(Category)
admin.site.register(About)
admin.site.register(Introduction)
admin.site.register(Term)
admin.site.register(Customer)
admin.site.register(Brokers)
admin.site.register(Email)
admin.site.register(Number)
admin.site.register(Address)
admin.site.register(Social)
admin.site.register(Subscriber)
admin.site.register(Newsletter)
admin.site.register(Announcement)


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)


send_newsletter.short_description = "Send selected Newsletters to all subscribers"


class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]


def send_signal(modeladmin, request, queryset):
    for signal in queryset:
        signal.send(request)


send_signal.short_description = "Send selected Signals to Customers"


class SignalsAdmin(admin.ModelAdmin):
    actions = [send_signal]


