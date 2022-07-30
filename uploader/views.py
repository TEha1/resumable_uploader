import hashlib
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from uploader.serializers import ResumableGETSerializer, ResumablePOSTSerializer

media_dir = settings.MEDIA_ROOT


def uploader_view(request):
    if request.POST:
        js_hex = request.POST["hex"]
        file0 = request.FILES.get("image")
        buffer0 = file0.read()
        hex = hashlib.md5(buffer0).hexdigest()

    return render(request, "uploader.html", {})


class ResumableUploadAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = ResumableGETSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resumable_identifier = data["resumableIdentifier"]
        resumable_filename = data["resumableFilename"]
        resumable_chunk_number = data["resumableChunkNumber"]

        # chunk folder path based on the parameters
        temp_dir = media_dir / resumable_identifier

        # chunk path based on the parameters
        chunk_file = temp_dir / get_chunk_name(
            resumable_filename, resumable_chunk_number
        )

        if not os.path.isfile(chunk_file):
            return Response("Not found", status=404)

        # Let resumable.js know this chunk already exists
        return Response("OK")

    def post(self, request, *args, **kwargs):
        serializer = ResumablePOSTSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resumable_identifier = data["resumableIdentifier"]
        resumable_total_chunks = data["resumableTotalChunks"]
        resumable_chunk_number = data["resumableChunkNumber"]
        resumable_file_name = data["resumableFilename"]
        chunk_data = data["file"]

        # make our temp directory
        temp_dir = media_dir / resumable_identifier
        if not os.path.isdir(temp_dir):
            try:
                os.makedirs(temp_dir, 0o777)
            except Exception as e:
                print(e)

        # save the chunk data
        chunk_name = get_chunk_name(resumable_file_name, resumable_chunk_number)
        chunk_file = temp_dir / chunk_name
        default_storage.save(chunk_file, ContentFile(chunk_data.read()))

        # check if the upload is complete
        chunk_paths = [
            temp_dir / get_chunk_name(resumable_file_name, x)
            for x in range(1, resumable_total_chunks + 1)
        ]
        is_upload_complete = all([os.path.exists(p) for p in chunk_paths])
        errors = []
        if is_upload_complete and chunk_paths:
            target_file_name = media_dir / resumable_file_name
            with open(target_file_name, "ab") as target_file:
                for p in chunk_paths:
                    stored_chunk_file_name = p
                    try:
                        with open(stored_chunk_file_name, "rb") as stored_chunk_file:
                            target_file.write(stored_chunk_file.read())
                            # os.unlink(stored_chunk_file_name)
                            stored_chunk_file.close()
                    except Exception as e:
                        errors.append(e)
                        continue
            target_file.close()
            print("Errors: ", errors)
            try:
                os.rmdir(temp_dir)
            except Exception as e:
                print("error = ", e)

        return Response("OK")


def get_chunk_name(uploaded_filename, chunk_number):
    return uploaded_filename + "_part_%03d" % chunk_number
