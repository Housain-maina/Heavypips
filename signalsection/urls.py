from django.urls import path
from . import views
from .views import Dashboard, SignalCreateView, SignalDeleteView, SignalUpdateView, AnnouncementCreateView, UserSignalsListView


urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:email>/', UserSignalsListView.as_view(), name='user-signals'),
    path('signal/<int:pk>/update/', SignalUpdateView.as_view(), name='signal-update'),
    path('signal/new/', SignalCreateView.as_view(), name='signal-create'),
    path('signal/<int:pk>/delete/', SignalDeleteView.as_view(), name='signal-delete'),
    path('about-us/', views.about, name='about'),
    path('introduction/', views.introduction, name='introduction'),
    path('brokers/', views.brokers, name='brokers'),
    path('charts/', views.charts, name='charts'),
    path('terms-of-use/', views.terms, name='terms'),
    path('privacy-policy/', views.terms, name='privacy'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('announcement/new/', AnnouncementCreateView.as_view(), name='announcement'),
    path('signal-subscription/', views.signalsub, name='signalsub'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),
    path('newsletter/', views.newsletter, name='newsletter'),

]
