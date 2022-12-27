from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from user.views import LogoutView, UserView

router = DefaultRouter()
router.register(prefix='Usuario', viewset=UserView, basename='Usuario')
router.register(prefix='token/logout', viewset=LogoutView, basename='token_logout')



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]