from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('core.urls')),
    path('auth/', include('core.urls'))
]

urlpatterns += [
    path('', RedirectView.as_view(url='/index')),
]