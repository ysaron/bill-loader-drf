import random


services = {
    1: 'консультация',
    2: 'лечение',
    3: 'стационар',
    4: 'диагностика',
    5: 'лаборатория',
}


def random_classifier(service_raw: str) -> dict:
    """
    :param service_raw: не используется здесь
    :return: словарь, распаковываемый в Model.create()
    """
    class_, name = random.choice(list(services.items()))
    return {
        'cls': class_,
        'name': name,
    }
