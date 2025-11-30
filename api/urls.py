from django.urls import path, include
from api.routers import router
from api.views import test_api, SongListAPIView, SongViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# ProductList

urlpatterns = [
    path('test/', test_api),
    path('test/<int:pk>/', test_api),
    path('Song', SongListAPIView.as_view()),
    path('', include(router.urls))
    # path('products/', ProductList.as_view(), name="products"),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]