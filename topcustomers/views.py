from copy import deepcopy

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from topcustomers.models import Customer
from topcustomers.serializers import CustomerSerializer


class TopCustomersViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        file_name = kwargs.get('file_name')
        customers = Customer.objects.filter(file_name=file_name).order_by('-spent_money')[0:5]

        """
        Создается словарь со всеми камнями у кастомеров в виде множеств. Далее для какждого кастомера
        проверяется пересечение множеств камней с другими. Если пересечение не пусто, то в говый словарь, который
        будет результатом работы, добавляется непустое множество для кастомера, пересечения которого проверяются. 
        Затем на основе полученноко словаря происходит замена камней в queryset (customers), 
        который будет отдан на клиент.
        """
        customers_dict_tmp = {}
        customers_dict = {}
        for customer in customers:
            customers_dict_tmp[customer.name] = set(customer.gems.split(','))
            customers_dict[customer.name] = set()

        for key1, val1 in customers_dict_tmp.items():
            for key2, val2 in customers_dict_tmp.items():
                if not key1 == key2:
                    if len(val1 & val2) > 0:
                        customers_dict[key1] |= val1 & val2

        print(customers_dict)
        for customer in customers:
            customer.gems = ','.join(customers_dict[customer.name])

        self.queryset = customers
        return Response(self.serializer_class(self.queryset, many=True, context={'request': request}).data)
