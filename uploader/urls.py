from django.urls import path

from uploader.views import uploader_view, ResumableUploadAPIView

urlpatterns = (
    path("", uploader_view, name="uploader"),
    path("resumable-upload/", ResumableUploadAPIView.as_view(), name="resumable_upload"),
)
