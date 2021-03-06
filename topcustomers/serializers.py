from rest_framework.serializers import ModelSerializer

from topcustomers.models import Customer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
