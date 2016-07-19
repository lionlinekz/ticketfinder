# coding: utf-8

from datetime import datetime
from api_requests import AuthoriseRequest, CloseSessionRequest, PlacesRequest, TrainPlacesRequest, BuyTicketRequest, PayOrderRequest, PassengerList
import base64


class Client(object):
    def __init__(self, api_usernumber, api_passmd5, id_terminal, id_service, request_url):
        self.credentials = {
            'api_usernumber': api_usernumber,
            'api_passmd5': api_passmd5,
            'id_terminal': id_terminal,
            'id_service': id_service,
            'request_url': request_url
        }
        self.guid = None

    def authorise(self):
        request = AuthoriseRequest(credentials = self.credentials)
        response = request.run()
        self.guid = response
        return response

    def close_session(self):
        payload = {
            'guid': self.guid
        }
        request = CloseSessionRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

    def get_places(self, from_station, to_station, date, time):
        payload = {
            'guid': self.guid,
            'from_station': from_station,
            'to_station': to_station,
            'date': date,
            'time': time
        }
        request = PlacesRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

    def get_train_places(self, from_station, to_station, date, time, train_number):
        payload = {
            'guid': self.guid,
            'from_station': from_station,
            'to_station': to_station,
            'date': date,
            'time': time,
            'train_number': base64.b64encode(train_number.encode("utf-8"))
        }
        request = TrainPlacesRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

    def buy_ticket(self, from_station, to_station, dep_date, train_number, car_type, car_number, 
                    car_class_service, req_seats_top, req_seats_bottom, req_seats_comp, req_bedding,
                    req_comp_type, req_seats_range, doc_type, doc_number, full_name, seat_type, seats_number):
        if seat_type in [u'Д', u'д']:
            tariff = u'<Tariff>Д</Tariff>'
        else:
            tariff = ''
        payload = {
            'guid':self.guid,
            'from_station': from_station,
            'to_station': to_station,
            'dep_date': dep_date,
            'train_number': base64.b64encode(train_number.encode("utf-8")),
            'car_type': base64.b64encode(car_type.encode("utf-8")),
            'car_number': base64.b64encode(car_number.encode("utf-8")),
            'car_class_service': base64.b64encode(car_class_service.encode("utf-8")),
            'req_seats_top': req_seats_top,
            'req_seats_bottom': req_seats_bottom,
            'req_seats_comp': base64.b64encode(req_seats_comp.encode("utf-8")),
            'req_bedding': req_bedding,
            'req_comp_type': base64.b64encode(req_comp_type.encode("utf-8")),
            'req_seats_range':req_seats_range,
            'doc_type': doc_type,
            'doc_number': doc_number,
            'full_name': full_name,
            'tariff': tariff,
            'seat_type': seat_type,
            'seats_number': seats_number
        }
        passengers_list = PassengerList(credentials = self.credentials, payload = payload)
        passengers = passengers_list.render()
        print passengers
        payload['passengers'] = base64.b64encode(passengers)
        request = BuyTicketRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

    def buy_multiple_ticket(self, from_station, to_station, dep_date, train_number, car_type, car_number, 
                    car_class_service, req_seats_top, req_seats_bottom, req_seats_comp, req_bedding,
                    req_comp_type, req_seats_range, doc_type, doc_number, full_name, seat_type, seats_number, passengers):
        if seat_type in [u'Д', u'д']:
            tariff = u'<Tariff>Д</Tariff>'
        else:
            tariff = ''
        payload = {
            'guid':self.guid,
            'from_station': from_station,
            'to_station': to_station,
            'dep_date': dep_date,
            'train_number': base64.b64encode(train_number.encode("utf-8")),
            'car_type': base64.b64encode(car_type.encode("utf-8")),
            'car_number': base64.b64encode(car_number.encode("utf-8")),
            'car_class_service': base64.b64encode(car_class_service.encode("utf-8")),
            'req_seats_top': req_seats_top,
            'req_seats_bottom': req_seats_bottom,
            'req_seats_comp': base64.b64encode(req_seats_comp.encode("utf-8")),
            'req_bedding': req_bedding,
            'req_comp_type': base64.b64encode(req_comp_type.encode("utf-8")),
            'req_seats_range':req_seats_range,
            'doc_type': doc_type,
            'doc_number': doc_number,
            'full_name': full_name,
            'tariff': tariff,
            'seat_type': seat_type,
            'seats_number': seats_number,
            'passengers':passengers
        }
        passengers_list = PassengerList(credentials = self.credentials, payload = payload)
        passengers = passengers_list.render()
        print passengers
        payload['passengers'] = base64.b64encode(passengers)
        request = BuyTicketRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

    def pay_order(self, order_number):
        payload = {
            'guid':self.guid,
            'order_number': order_number
        }
        request = PayOrderRequest(credentials = self.credentials, payload = payload)
        response = request.run()
        return response

