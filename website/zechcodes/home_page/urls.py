from django.conf.urls import url
from home_page.views import home_page


urlpatterns = [
    url(r"^$", home_page, name="homepage"),
]
