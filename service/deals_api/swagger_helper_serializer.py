from rest_framework import serializers


class DealUploadSerializer(serializers.Serializer):
    deals = serializers.FileField()


class DealUpload200Serializer(serializers.Serializer):
    status = serializers.CharField()


class Error400Serializer(serializers.Serializer):
    status = serializers.CharField()
    desc = serializers.CharField()


class TopClientsParametersSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=False)
    finish_data = serializers.DateTimeField(required=False)


class TopClientsResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    spent_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    gems = serializers.ListSerializer(child=serializers.CharField())
