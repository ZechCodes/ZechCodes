from django.shortcuts import render
from django.conf import settings


def home_page(request):
    context = {"google_analytics_key": settings.GOOGLE_ANALYTICS_KEY}
    return render(request, "home_page.html", context)
