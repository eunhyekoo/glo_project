from django.urls import path
from clients_feedback_tracker_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('healthz', views.ApiHealthCheckView.as_view()),
    path('feedback/read/<str:databaseId>', views.GetAllNotionFeedbacks.as_view()),
    path('feedback/create/management', views.CreateManagement.as_view()),
    path('feedback/create', views.CreateClientFeedbackRegistry.as_view()),
    path('feedback/create/translation', views.GetTranslationInfoViewSet.as_view({'post':'create'})),
    path('memsource/translation', views.GetAllMemousrceData.as_view()),
    path('memsource/new/translation',views.GetNewestMemsourceData.as_view())
]