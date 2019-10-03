import random
from datetime import datetime
from json import load, loads

import faker

fake = faker.Faker('pt_BR')

def fake_job_type():
    return 'home'


def fake_email():
    return fake.email()


def fake_expire_year():
    return int(fake.credit_card_expire(start="now", end="+10y", date_format="%y"))


def fake_expire_month():
    return int(fake.credit_card_expire(start="now", end="+10y", date_format="%m"))


def fake_cpf():
    return int(random.randint(10000000000, 99999999999))


def fake_cvv():
    return int(fake.credit_card_security_code(card_type=None))


def fake_name():
    return fake.name().upper()

def fake_birthdate():
    return '2019-09-26T17:59:33.150Z'


def fake_longitude():
    longitude = random.uniform(-46.622672, -46.699233)
    return float(longitude)


def fake_latitude():
    latitude = random.uniform(-23.554554, -23.613078)
    return float(latitude)


def fake_timestamp():
    hour = random.choice(list(range(8, 22)))
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day + 1
    return datetime(year, month, day, hour).timestamp()


def fake_first_name():
    return fake.name().split(' ')[0]


def fake_last_name():
    return fake.name().split(' ')[1]


def fake_street():
    return 'rua quata'


def fake_city():
    return 'sao paulo'


def fake_neighborhood():
    return random.choice(['itaim', 'jardins', 'vila olimpia'])


def fake_complement():
    return 300


def fake_state():
    return 'SP'


def fake_duration():
    return random.choice([1, 2, 3, 4, 5]) * 3600


def fake_location():
    return (fake_latitude(), fake_longitude())


KNOW_FUNCTIONS = {
    'jobType': fake_job_type,
    'cpf': fake_cpf,
    'number': fake.credit_card_number,
    'cvc': fake_cvv,
    'email': fake_email,
    'name': fake_name,
    'expiryMonth': fake_expire_month,
    'expiryYear': fake_expire_year,
    'latitude': fake_latitude,
    'longitude': fake_longitude,
    'firstName': fake_first_name,
    'lastName': fake_last_name,
    'complement': fake_complement,
    'city': fake_city,
    'neighborhood': fake_neighborhood,
    'street': fake_street,
    'state': fake_state,
    'duration': fake_duration,
    'date': fake_timestamp,
    'location': fake_location,
    'birthdate': fake_birthdate
}


def make_payload(file_path):
    with open(file_path) as schema_file:
        json = loads(schema_file.read())
    return parse_obj(json)


def parse_string(obj, name):
    if 'enum' in obj:
        return random.choice(obj['enum'])
    if name in KNOW_FUNCTIONS:
        return str(KNOW_FUNCTIONS[name]())
    return 'a'


def parse_number(obj, name):
    if 'enum' in obj:
        return random.choice(obj['enum'])
    if name in KNOW_FUNCTIONS:
        return KNOW_FUNCTIONS[name]()
    return 1


def parse_boolean():
    return True


def parse_obj(obj):
    ret_obj = {}
    for key in obj['properties']:
        if 'object' in obj['properties'][key]['type']:
            ret = parse_obj(obj['properties'][key])
        elif 'array' in obj['properties'][key]['type']:
            ret = parse_array(obj['properties'][key])
        elif 'string' in obj['properties'][key]['type']:
            ret = parse_string(obj['properties'][key], key)
        elif 'number' in obj['properties'][key]['type']:
            ret = parse_number(obj['properties'][key], key)
        elif 'boolean' in obj['properties'][key]['type']:
            ret = parse_boolean()
        ret_obj[key] = ret
    return ret_obj


def parse_array(obj):
    array = []
    for item in obj['items']:
        if 'object' in item['type']:
            ret = parse_obj(item)
        elif 'array' in item['type']:
            ret = parse_array(item)
        elif 'string' in item['type']:
            ret = parse_string(obj, None)
        elif 'number' in item['type']:
            ret = parse_number(obj, None)
        elif 'boolean' in item['type']:
            ret = parse_boolean()
        if 'minItems' not in obj:
            array.append(ret)
        else:
            min_items = int(obj['minItems'])
            for i in range(min_items):
                array.append(ret)
    return array

