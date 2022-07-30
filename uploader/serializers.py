from rest_framework import serializers


class ResumableGETSerializer(serializers.Serializer):
    resumableIdentifier = serializers.CharField()
    resumableFilename = serializers.CharField()
    resumableChunkNumber = serializers.IntegerField()


class ResumablePOSTSerializer(serializers.Serializer):
    resumableTotalChunks = serializers.IntegerField()
    resumableChunkNumber = serializers.IntegerField(default=1)
    resumableFilename = serializers.CharField(default="error")
    resumableIdentifier = serializers.CharField(default="error")
    file = serializers.FileField()

