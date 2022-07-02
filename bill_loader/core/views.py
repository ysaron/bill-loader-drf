from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from django_filters.rest_framework import DjangoFilterBackend

from .services.documents import save_from_excel
from .services.filters import BillFilter
from .models import Client, Bill
from .serializers import ClientSerializer, BillSerializer


class ExcelUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format_=None):
        if 'file' not in request.data:
            raise ParseError('No file received')
        document = request.data['file']
        save_from_excel(document, filename=filename)

        return Response(status=status.HTTP_201_CREATED)


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BillFilter
