import os
import json
import requests


def parse_longitude_and_width():
    with open('result.json', 'r') as file:
        data = json.loads(file.read())

    position = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')

    longitude = position[0]
    width = position[1]

    return dict(longitude=longitude, width=width)


def work_with_json(address):
    token = '93a0b765-6f98-41d0-996a-e6fb7ac78b0d'
    url_geo = f'https://geocode-maps.yandex.ru/1.x/'

    url = url_geo + f'?apikey={token}&geocode={address}&format=json'

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.status_code)

    except Exception as err:
        return err

    else:
        with open('result.json', 'w') as file:
            file.write(response.text)

    return response.status_code


def work_with_map(longitude, width, address):

    token = '93a0b765-6f98-41d0-996a-e6fb7ac78b0d'
    url_static = 'https://static-maps.yandex.ru/1.x/'

    if len(address.split()) > 3:
        spn = [0.01, 0.01]
    elif len(address.split()) > 1:
        spn = [0.05, 0.05]
    else:
        spn = [0.2, 0.2]
    url = url_static + f'?apikey={token}&ll={longitude},{width}&' \
                       f'spn={spn[0]},{spn[1]}&l=map'

    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.status_code)

    except Exception as err:
        return err

    else:
        with open('map.jpg', 'wb') as file:
            file.write(response.content)

    return response.status_code


def main():
    print('Введите адрес: ', end='')
    address = input()
    print()
    city_info = work_with_json(address)

    if city_info == 200:
        position = parse_longitude_and_width()
        print(f'Долгота: {position["longitude"]}')
        print(f'Широта: {position["width"]}')
        city_map = work_with_map(position['longitude'], position['width'], address)

        if city_map != 200:
            print('Не удалось получить изображение!')

    else:
        print('Информация об адресе не была получена!')


main()
