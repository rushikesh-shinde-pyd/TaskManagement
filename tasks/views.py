# Standard library imports
import logging
import sys

# Django imports
from django.conf import settings
from django.core.cache import cache

# Third-party imports
from rest_framework import permissions, throttling, pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Local imports
from .models import User, Task
from .utils import set_cache
from .serializers import UserSerializer, TaskSerializer
from .constants import RESPONSE_500, CACHE_USER_KEY, CACHE_TASK_KEY


logger = logging.getLogger(__name__)


class RegisterView(APIView):
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)

    def get(self, request):
        try:
            cache_key = CACHE_USER_KEY.format(request.user.id)
            cached_details = cache.get(cache_key)

            if cached_details:
                return Response(cached_details)

            user_obj = User.objects.get(username=request.user.username)
            serializer = UserSerializer(user_obj)
            set_cache(cache_key, serializer.data)

            return Response(serializer.data)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in RegisterView GET: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                cache_key = CACHE_USER_KEY.format(request.user.id)
                cache.delete(cache_key)

                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=201)

            return Response(serializer.errors, status=400)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in RegisterView POST: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def patch(self, request):
        try:
            user_obj = User.objects.get(username=request.user.username)
            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                cache_key = CACHE_USER_KEY.format(request.user.id)
                cache.delete(cache_key)

                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in RegisterView PATCH: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def get_permissions(self):
        if self.request.method in ('GET', 'PUT'):
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

class TaskListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = pagination.PageNumberPagination

    def get(self, request):
        try:
            user = request.user
            cache_key = CACHE_TASK_KEY.format(user.id)
            cached_tasks = cache.get(cache_key)

            if cached_tasks:
                return Response(cached_tasks)

            paginator = self.pagination_class()
            tasks = Task.objects.filter(user=user)
            results = paginator.paginate_queryset(tasks, request)
            serializer = TaskSerializer(results, many=True)
            response = paginator.get_paginated_response(serializer.data)

            set_cache(cache_key, response.data)
            return response
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in TaskListCreateView GET: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def post(self, request):
        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                cache_key = CACHE_TASK_KEY.format(request.user.id)
                cache.delete(cache_key)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in TaskListCreateView POST: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def get_task(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        try:
            task = self.get_task(pk, request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except NotFound:
            return Response({"detail": "Task not found."}, status=404)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in TaskDetailView GET: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def patch(self, request, pk):
        try:
            task = self.get_task(pk, request.user)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                cache_key = CACHE_TASK_KEY.format(request.user.id)
                cache.delete(cache_key)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except NotFound:
            return Response({"detail": "Task not found."}, status=404)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in TaskDetailView PATCH: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)

    def delete(self, request, pk):
        try:
            task = self.get_task(pk, request.user)
            task.delete()
            cache_key = CACHE_TASK_KEY.format(request.user.id)
            cache.delete(cache_key)
            return Response({'detail': 'Content deleted.'}, status=204)
        except NotFound:
            return Response({"detail": "Task not found."}, status=404)
        except Exception as e:
            _, __, tb = sys.exc_info()
            logger.error(f"Error in TaskDetailView DELETE: {str(e)} at lineno: {tb.tb_lineno}")
            return Response(RESPONSE_500, status=500)


# Convert Class-Based Views to View Functions
RegisterView = RegisterView.as_view()
TaskListCreateView = TaskListCreateView.as_view()
TaskDetailView = TaskDetailView.as_view()