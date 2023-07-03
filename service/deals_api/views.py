import csv
from datetime import datetime

from django.db.models import Sum
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from deals_api import swagger_helper_serializer
from deals_api.models import Deal


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.DealUploadSerializer,
    responses={
        200: swagger_helper_serializer.DealUpload200Serializer,
        400: swagger_helper_serializer.Error400Serializer,
    }
)
class DealUploadView(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('deals')
        if file:
            try:
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                deals = []
                for row in reader:
                    date_str = row['date']
                    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                    deal = Deal(
                        customer=row['customer'],
                        item=row['item'],
                        total=float(row['total']),
                        quantity=int(row['quantity']),
                        date=date
                    )
                    deals.append(deal)
                Deal.objects.bulk_create(deals)
                return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'status': 'Error', 'desc': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'Error', 'desc': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['GET'],
    parameters=[swagger_helper_serializer.TopClientsParametersSerializer],
    responses={
        200: swagger_helper_serializer.TopClientsResponseSerializer,
        400: swagger_helper_serializer.Error400Serializer
    }
)
class TopClientsView(APIView):
    permission_classes = []
    parser_classes = [JSONParser]

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        start_date = request.query_params.get('start_date')
        finish_date = request.query_params.get('finish_date')
        if start_date and finish_date:
            start_date = parse_datetime(start_date)
            finish_date = parse_datetime(finish_date)
            if finish_date < start_date:
                return Response(
                    {'status': 'Error', 'desc': 'The start date cannot be greater than the end date.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            top_clients = Deal.objects.filter(date__gte=start_date, date__lte=finish_date).values('customer').annotate(
                spent_money=Sum('total')
            ).order_by('-spent_money')[:5]
        else:
            top_clients = Deal.objects.values('customer').annotate(
                spent_money=Sum('total')
            ).order_by('-spent_money')[:5]

        top_clients_data = []
        for client in top_clients:
            username = client['customer']
            spent_money = client['spent_money']
            gems = Deal.objects.filter(customer=username).values_list('item', flat=True).distinct()
            gems = list(gems)

            top_clients_data.append({
                'username': username,
                'spent_money': spent_money,
                'gems': gems
            })

        response_data = {'response': top_clients_data}
        return Response(response_data, status=status.HTTP_200_OK)