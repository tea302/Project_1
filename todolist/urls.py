
from django.contrib import admin
from django.db import router
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from network.views import RetailViewSet

router.register('api/retail', RetailViewSet)


# ----------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('core.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

urlpatterns += router.urls
