import pandas

from django.db import transaction
from rest_framework.exceptions import APIException

from ..models import Bill, Client, Organization, Service
from .classifier import random_classifier
from .fraud_detector import random_detector


def handle_bills(data: pandas.DataFrame):
    """ Сохраняет в БД данные о счетах из датафрейма """

    if any([
        not Client.objects.all().exists(),
        not Organization.objects.all().exists(),
    ]):
        raise APIException('Данные о клиентах и организациях не загружены')

    for index, row in data.iterrows():
        service, _ = Service.objects.get_or_create(**random_classifier(row['service']))
        client = Client.objects.get(name=row['client_name'])
        organization = Organization.objects.get(name=row["client_org"])

        Bill.objects.create(
            client=client,
            organization=organization,
            number=row['№'],
            sum=float(row['sum']),
            date=row['date'],
            service=service,
            fraud_score=random_detector(row['service']),
        )


def handle_client_org(client_df: pandas.DataFrame, org_df: pandas.DataFrame):
    """ Сохраняет в БД данные о клиентах и организациях из датафрейма """

    for index, row in client_df.iterrows():
        print(row['name'])
        Client.objects.get_or_create(name=row['name'])

    for index, row in org_df.iterrows():
        print(f'{row["client_name"]} -- {row["name"]} -- {row["address"]}')
        with transaction.atomic():
            client, _ = Client.objects.get_or_create(name=row["client_name"])
            address = row["address"]
            Organization.objects.get_or_create(
                name=row["name"],
                client=client,
                address=f'Адрес: {address}' if address else '',
            )


def save_from_excel(doc, filename: str):
    """ Делегирует обработку файла соответствующей функции """
    match filename:
        case 'client_org.xlsx':
            client_data = pandas.read_excel(doc, sheet_name='client')
            org_data = pandas.read_excel(doc, sheet_name='organization')
            handle_client_org(client_data, org_data)
        case 'bills.xlsx':
            bills_data = pandas.read_excel(doc, sheet_name=0)
            handle_bills(bills_data)
        case _:
            raise ValueError('Недопустимое имя файла')
