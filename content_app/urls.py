from django.urls import path
from .views import HomePage, FeedbackView
app_name = 'content_app'
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contact/', FeedbackView.as_view(), name='contact'),
]
