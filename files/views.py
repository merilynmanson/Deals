from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import GenericViewSet, mixins
from files.models import File
from files.serializers import FileSerializer
from files.utils import csv_to_db


class FilesViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser, )

    def perform_create(self, serializer):
        file_data = self.request.data.get('file')
        file_obj = serializer.save(file=file_data)
        csv_to_db(file_obj.file)
