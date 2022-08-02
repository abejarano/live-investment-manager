from django.urls import path

from apps.crypto.views import Price

urlpatterns = [
    path('task', Price.as_view())
]
