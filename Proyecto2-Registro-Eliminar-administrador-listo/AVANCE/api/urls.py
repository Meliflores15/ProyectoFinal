from django.urls import path,include
from rest_framework import serializers,routers
from .import views
from .views import ProduccionesViewSet, ProductoViewSet,PlantaViewSet



router= routers.DefaultRouter()
router.register('producciones',views.ProduccionesViewSet)
urlpatterns=[
    path('',include(router.urls))
]

router.register('producto',views.ProductoViewSet)
urlpatterns=[
    path('',include(router.urls))
]

router.register('planta',views.PlantaViewSet)
urlpatterns=[
    path('',include(router.urls))
]