from rest_framework import routers
from .api import ProductoViewSet

router = routers.DefaultRouter()

router.register('productos', ProductoViewSet, 'productos')

urlpatterns = router.urls