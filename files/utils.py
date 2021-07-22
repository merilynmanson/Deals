import csv
from django.utils.timezone import datetime

from files.models import File
from topcustomers.models import Deal, Customer


def csv_to_db(file_data):
    """
    Функция сохраняет данные из csv файла в таблицы БД customers и deals
    :param file_data: Данные файла: имя и тд.
    :return: Статус: OK или Error с описанием ошибки
    """
    file_path = file_data.path
    file_name = file_data.name
    with open(file_path, encoding='utf8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        try:
            for row in reader:
                # Если читаемый ряд в файле состоит не из 5 элементов, то исключение
                if not len(row) == 5:
                    raise Exception('Incorrect data row. Details: wrong separation - there must be 5 fields')

                if not first_row:
                    customer_name = row[0]  # Extract customer's name
                    item = row[1]

                    try:
                        total = int(row[2])
                        quantity = int(row[3])
                    except Exception as e:
                        raise Exception('Incorrect data row. Details: ' + str(e))

                    try:
                        date = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f")
                    except Exception as e:
                        raise Exception('Incorrect data row. Details: ' + str(e))

                    new_deal = Deal(
                        customer=customer_name,
                        item=item,
                        total=total,
                        quantity=quantity,
                        date=date,
                        file_name=file_name
                    )

                    try:
                        customer = Customer.objects.get(name=customer_name, file_name=file_name)
                    except Customer.DoesNotExist:
                        customer = None

                    if customer:
                        customer.spent_money += total
                        gems = set(customer.gems.split(','))
                        gems.add(item)
                        customer.gems = ','.join(gems)
                    else:
                        customer = Customer(
                            name=customer_name,
                            spent_money=total,
                            gems=item,
                            file_name=file_name
                        )
                    new_deal.save()
                    customer.save()
                else:
                    first_row = False
        except Exception as e:
            File.objects.get(file=file_data).delete()
            return {'Status': {'Error': str(e)}}

        return {'Status': 'OK'}
