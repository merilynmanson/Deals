from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from files.models import File
from files.serializers import FileSerializer
from files.utils import csv_to_db


class FilesViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    csv_to_db_result = {}  # Хранит результат сохранения данных файла в БД

    def perform_create(self, serializer):
        file_data = self.request.data.get('file')
        file_obj = serializer.save(file=file_data)
        self.csv_to_db_result = csv_to_db(file_obj.file)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if self.csv_to_db_result['Status'] == 'OK':
            return Response(self.csv_to_db_result, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(self.csv_to_db_result, status=status.HTTP_400_BAD_REQUEST, headers=headers)
