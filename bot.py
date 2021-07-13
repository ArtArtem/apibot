import vk_api
import time
import requests
import random

vk = vk_api.VkApi(token="65ef388598665736f67f917f93b7c8b4e03312698ef52ba3c752b47a91adc8c3c8bc474da67f12bcda891")

vk._auth_token()


def photo(user_id):
    print(1)
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open('stars.jpg', 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send",
              {"peer_id": user_id, "message": "Фотка", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})
    print(2)


def address(name):
    print(name)
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(name)

    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            toponym_coodrinates = toponym["Point"]["pos"]
            a = ''
            a = a.join([toponym_address + ', ' + index, ", имеет координаты: ", toponym_coodrinates])
            return a
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return 2
    except Exception as e:
        print(e)
        print("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")
        return e


def metro(name):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}.&format=json".format(name)
    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_coord = toponym["Point"]["pos"]
            a = requests.get( \
                "https://geocode-maps.yandex.ru/1.x/?geocode={}&kind=metro&format=json&results=1".format(toponym_coord)) \
                .json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["text"]
            return a
        else:
            print("ошибка")

    except Exception:
        print("ошибка")


def mapta(name, id):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(name)

    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            cords = toponym["Point"]["pos"].split()

    except:
        print("ошибка")

    response = None
    try:
        map_request = "https://static-maps.yandex.ru/1.x/?ll=0%2C0&z=1&pt={}%2C{},ya_ru&size=450,450&l=sat".format(
            cords[0], cords[1])

        response = requests.get(map_request)

        if not response:
            print("ошибка")
    except:
        print("ошибка")

    map_file = "map123.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        pass

    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open('map123.png', 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send",
              {"peer_id": id, "message": "успех", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})


def translateenru(slovo, en):
    if en == 1:
        response = requests.get(
            "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang=en-ru&text={}".format(
                'dict.1.1.20190419T175719Z.89e9a7058513775c.6e06ee33694de12cc661fc96d34ad1ea6b0372c0', slovo))
    else:
        response = requests.get(
            "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang=ru-en&text={}".format(
                'dict.1.1.20190419T175719Z.89e9a7058513775c.6e06ee33694de12cc661fc96d34ad1ea6b0372c0', slovo))
    json_response = response.json()
    return json_response["def"][0]["tr"][0]["text"]


def zagadka(num, id):
    if num == 1:
        a = vk.method("photos.getMessagesUploadServer")
        b = requests.post(a['upload_url'], files={'photo': open('zag1.jpg', 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
        vk.method("messages.send",
                  {"peer_id": id, "message": "успех", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})

    if num == 2:
        a = vk.method("photos.getMessagesUploadServer")
        b = requests.post(a['upload_url'], files={'photo': open('zag2.jpg', 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
        vk.method("messages.send",
                  {"peer_id": id, "message": "успех", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})

    if num == 3:
        a = vk.method("photos.getMessagesUploadServer")
        b = requests.post(a['upload_url'], files={'photo': open('zag3.jpg', 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
        vk.method("messages.send",
                  {"peer_id": id, "message": "успех", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})

    return num


def main():
    while True:

        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower() == "начать":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Привет, я ВК бот на все случаи жизни, спроси меня <<что ты можешь>>, чтобы узнать о моих возможностях!"})
            if body.lower() == "что ты можешь":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Напиши <<гео>>, если хочешь задать вопрос, свазанный с географическими объектами, адресами, улицами, станциями метро. Напиши <<перевод>>, если хочешь получить перевод слов. Напиши <<загадка>>, если хочешь поломать голову."})
            if body.lower() == "гео":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Напиши <<полный адрес>>, <<станция метро>> или <<карта земли с меткой>>, чтобы активировать соответствующую функцию."})
            if body.lower() == "полный адрес":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Введи запрос с '#1' в начале сообщения, например, '#1Красная площадь'."})
            if body.lower() == "станция метро":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Введи запрос с '#2' в начале сообщения, например, '#2Красная площадь'."})
            if body.lower() == "карта земли с меткой":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Введи запрос с '#3' в начале сообщения, например, '#3Красная площадь'."})
            if body.lower()[:2:] == "#1":
                poisk = body.lower()[2::]
                vk.method("messages.send", {"peer_id": id, "message": address(poisk)})
            if body.lower()[:2:] == "#2":
                poiskmetro = body.lower()[2::]
                vk.method("messages.send", {"peer_id": id, "message": metro(poiskmetro)})
            if body.lower()[:2:] == "#3":
                kard = body.lower()[2::]
                mapta(kard, id)
                # vk.method("messages.send", {"peer_id": id, "message": mapta(kard, id)})
            if body.lower() == "перевод":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Напиши слово с '#4', если хочешь перевести его с русского на английский, например, <<#4МОРОЖЕНОЕ>>, или c '#5' в начале, если хочешь перевести слово с английского на русский, например, <<#5CHOCOLATE>>."})
            if body.lower()[:2:] == "#4":
                slovo = body.lower()[2::]
                vk.method("messages.send", {"peer_id": id, "message": translateenru(slovo, 0)})

            if body.lower()[:2:] == "#5":
                slovo = body.lower()[2::]
                vk.method("messages.send", {"peer_id": id, "message": translateenru(slovo, 1)})

            if body.lower() == "загадка":
                num = random.choice([1, 2, 3])
                zagadka(num, id)
                if num == 1:
                    vk.method("messages.send", {"peer_id": id,
                                                "message": "Напиши ответ с 'z1' в начале сообщения, например <<z1ВОРОНА>>"})
                if num == 2:
                    vk.method("messages.send", {"peer_id": id,
                                                "message": "Напиши ответ с 'z2' в начале сообщения, например <<z2ВОРОНА>>"})
                if num == 3:
                    vk.method("messages.send", {"peer_id": id,
                                                "message": "Напиши ответ с 'z3' в начале сообщения, например <<z3ВОРОНА>>"})
            if body.lower()[:2:] == "z1":
                slovo = body.lower()[2::]
                if slovo == 'нет':
                    vk.method("messages.send", {"peer_id": id, "message": 'Правильно!'})
            if body.lower()[:2:] == "z2":
                slovo = body.lower()[2::]
                if slovo == 'темная тема' or slovo == 'тёмная тема':
                    vk.method("messages.send", {"peer_id": id, "message": 'Правильно!'})
            if body.lower()[:2:] == "z3":
                slovo = body.lower()[2::]
                if slovo == '6':
                    vk.method("messages.send", {"peer_id": id, "message": 'Правильно!'})

            if body.lower() == "?":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Мои функции: <<полный адрес>>, <<станция метро>>, <<карта земли с меткой>>, <<перевод>>, <<загадка>>"})


while True:
    try:
        main()
    except Exception as e:
        time.sleep(1)
