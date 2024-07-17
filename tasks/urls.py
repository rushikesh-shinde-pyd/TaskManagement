# Django imports
from django.urls import path

# Third-party imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Local imports
from .views import RegisterView, TaskListCreateView, TaskDetailView

app_name = 'tasks'

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListCreateView, name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView, name='task-detail'),
]
