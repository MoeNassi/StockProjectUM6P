from rest_framework_nested import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register('school', SchoolViewSet, basename='school')
router.register('stock', StockViewSet)
router.register('users', UserViewSet)

nestedRoute = routers.NestedDefaultRouter(router, 'school', lookup='school')
nestedRoute.register('stock', StocksPerSchoolViewSet, basename='stock-list')

urlpatterns = router.urls + nestedRoute.urls