
from Constant import BASE_URL
import pytest
import requests

"""Вынесли запрос по айди в отдельную функцию, использовал 1 раз в удаляем букинг по айди"""
def get_booking_by_id(session, booking_id):
    return session.get(f'{BASE_URL}/booking/{booking_id}')

class TestBookings():


    def test_create_booking(self, auth_session, booking_data, put_data):

        """Создаем букинг"""
        create_booking=auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code==200, "Ошибка при создании букинга"

        """Получаем букинг Айди у созданного букинга"""

        booking_id=create_booking.json().get("bookingid")
        assert booking_id is not None, "Айди брони не наеден в ответе"

        """Проверяем что отправленные данные соответствуют полученным"""
        assert create_booking.json()["booking"]['firstname'] == booking_data['firstname'], 'Заданное имя не совпадает'
        assert create_booking.json()["booking"]['totalprice'] == booking_data['totalprice'], 'Заданная стоимость не совпадает'

        """Получаем все букинги, смотрим что список есть и он не пустой + проверяем что наш букинг попал в список"""
        get_booking_all = auth_session.get(f'{BASE_URL}/booking')
        assert isinstance(get_booking_all.json(), list), "В ответе не список"
        assert len(get_booking_all.json()) > 0, "Список не пустой"
        assert any(
            item.get('bookingid') == booking_id for item in get_booking_all.json()
        )
        """Получаем все букинги, по параметрам имя (имя указанное при отправке пакетов)"""
        get_booking_name = auth_session.get(f'{BASE_URL}/booking', params={'firstname' : booking_data["firstname"]})
        assert get_booking_name.status_code == 200
        assert isinstance(get_booking_name.json(), list), "В ответе не список"
        assert len(get_booking_name.json()) > 0, "Список не пустой"
        assert any(
            item.get("bookingid") == booking_id for item in get_booking_name.json()
        )
        """Получаем все букинги, по параметрам имя и фамилия (данные указанное при отправке пакетов)"""
        get_booking_fullname = auth_session.get(f'{BASE_URL}/booking', params = {'firstname': booking_data["firstname"], 'lastname' : booking_data["lastname"]})
        assert get_booking_fullname.status_code == 200
        assert isinstance(get_booking_fullname.json(), list), "В ответе не список"
        assert any(
            item.get("bookingid") == booking_id for item in get_booking_name.json()
        )
        """Получаем все букинги, по параметрам заселение и выселение (данные указанное при отправке пакетов, сделана мягкая првоерка с инфо сообщением)"""
        get_booking_check=auth_session.get(f'{BASE_URL}/booking', params={'checkin' : booking_data['bookingdates']['checkin'], 'checkout': booking_data['bookingdates']['checkout']})
        assert  isinstance(get_booking_check.json(), list)
        if get_booking_check.status_code == 200:
            bookings = get_booking_check.json()
            if not any(item.get("bookingid") == booking_id for item in bookings):
                print(f'[INFO] booking_id{booking_id} не найден в выдаче по датам — возможно, фильтр не работает.')

        """Получаем букинг по айди"""
        get_booking=auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert get_booking.status_code == 200, "Букинг не найден"
        assert get_booking.json()['firstname'] == create_booking.json()["booking"]['firstname'], "Запрос не совпадает с ответом"

        """Обновляем частично букинг по айди и проверяем ответ и запись в базу"""
        patch_booking=auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json={"firstname" : "IVAN", "lastname" : "GROZNY"})
        assert patch_booking.status_code == 200, 'Данные не обновлены'
        assert patch_booking.json()['firstname'] == "IVAN"
        assert patch_booking.json()['lastname'] == "GROZNY"
        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert get_booking.json() == patch_booking.json()

        """Обновляем full букинг по айди и проверяем ответ и запись в базу"""
        put_booking=auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=put_data)
        assert put_booking.status_code == 200, 'Данные не обновлены'
        assert put_booking.json() == put_data, "Букинг не заменен"

        """Удаляем букинг по айди проверяем что удалилось через поиск по айди"""
        delite_booking=auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delite_booking.status_code == 201,  'Букинг не удалился'
        get_booking=get_booking_by_id(auth_session, booking_id)
        assert get_booking.status_code == 404, 'Букинг не удалился'


