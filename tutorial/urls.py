from django.urls import path

from tutorial import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),
    path('mailbox', views.mailbox, name='mailbox'),
    path('inbox', views.inbox, name='inbox'),
    path('outbox', views.outbox, name='outbox'),
    path('drafts', views.drafts, name='drafts'),
    ]
