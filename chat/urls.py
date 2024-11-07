from django.urls import path, include
from .views import ChatViewSet, GPTResponseListView, FileUploadView, CustomGPTViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('my-gpts', CustomGPTViewSet)
router.register('', ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<chat_id>/responses/list/', GPTResponseListView.as_view(), name='message-list'),
    path('<chat_id>/upload-file/', FileUploadView.as_view(), name='upload-file'),
]
