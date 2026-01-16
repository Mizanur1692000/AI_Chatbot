from django.urls import path
from .views import ChatView, SetEmailView

urlpatterns = [
    path('set_email/', SetEmailView.as_view(), name='set_email'),
    path('chat/', ChatView.as_view(), name='chat'),
]
