# drf yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# restframework
from rest_framework import permissions

# restframework_simplejwt
from rest_framework_simplejwt import views as jwt_views

# django
from django.urls import path, re_path


schema_view = get_schema_view(
    openapi.Info(
        title="Knight Meat Taste API",
        default_version="v1",
        description="Testing api endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tetobobo1@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = []


# API documentation
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]


# token and refresh tokem=n with jwt
urlpatterns += [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
