from django.urls import path
from . import views
from .api.views import AnalyzeWebpageAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('api/analyze/', AnalyzeWebpageAPIView.as_view(), name='api-analyze'),
]
