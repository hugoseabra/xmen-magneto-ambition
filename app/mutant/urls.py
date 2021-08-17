from rest_framework import routers

from app.mutant import viewsets

app_name = 'mutant'

router = routers.SimpleRouter()
router.register(r'stats', viewsets.StatisticsViewset, basename='stats')
router.register(r'mutant', viewsets.MutantViewset, basename='mutant')

urlpatterns = router.urls
