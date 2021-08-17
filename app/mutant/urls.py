from rest_framework import routers

from app.mutant import viewsets

router = routers.SimpleRouter()
router.register(r'stats', viewsets.StatisticsViewset)
router.register(r'mutant', viewsets.MutantViewset)

urlpatterns = router.urls
