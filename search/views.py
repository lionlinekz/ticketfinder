# coding=utf-8
from client.client import Client
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateformat import DateFormat
from ticketfinder import settings as conf
from models import Station, TrainSeat, Car, Ticket
from datetime import datetime
import json



def index(request):
	stations = Station.objects.all()
	context_dict = {'stations': stations}
	return render(request, 'search/index.html', context_dict)
	
def book(request):
	stations = Station.objects.all()
	context_dict = {'stations': stations}
	if request.method == 'POST':
		context_dict['message'] = u"Ваша заявка принята. Мы оповестим вас как только найдем подходящий по вашему запросу билет"
	return render(request, 'search/book.html', context_dict)
	
def get_trains(request):
	context_dict = {}
	if request.method == 'POST':
		from_station = request.POST.get('from_station')
		to_station = request.POST.get('to_station')
		date = request.POST.get('departure_date')
		departure_date = datetime.strptime(date, "%Y-%m-%d")
		client = Client(api_usernumber = conf.USER_NUMBER, api_passmd5 = conf.USER_PASSMD5, id_terminal = conf.ID_TERMINAL, id_service = conf.ID_SERVICE, request_url = conf.API_URL)
		df = DateFormat(departure_date)
		places = client.get_places(from_station, to_station, df.format('d.m.Y'), '0123')
		data = json.dumps(places, ensure_ascii=False)
		response_dict = json.loads(data)
		if 'status' in response_dict:
			context_dict['error'] = response_dict['message']
		else:
			context_dict = request_handler(response_dict)
		context_dict['data'] = data
		context_dict['from_station'] = Station.objects.get(code=from_station)
		context_dict['to_station'] = Station.objects.get(code=to_station)
		context_dict['departure_date'] = date
		context_dict['stations'] = Station.objects.all()
	return render(request, 'search/trains.html', context_dict)
	
def places(request):
	context_dict = {}
	if request.method == 'POST':
		from_station = request.POST.get('from_station')
		to_station = request.POST.get('to_station')
		date = request.POST.get('departure_date')
		time = request.POST.get('departure_time')
		train_number = request.POST.get('train_number')
		departure_date = datetime.strptime(date, "%Y-%m-%d")
		client = Client(api_usernumber = conf.USER_NUMBER, api_passmd5 = conf.USER_PASSMD5, id_terminal = conf.ID_TERMINAL, id_service = conf.ID_SERVICE, request_url = conf.API_URL)
		df = DateFormat(departure_date)
		places = client.get_train_places(from_station, to_station, df.format('d.m.Y'), time, train_number)
		data = json.dumps(places, ensure_ascii=False)
		response_dict = json.loads(data)
		if 'status' in response_dict:
			context_dict['error'] = response_dict['message']
		else:
			context_dict = place_handler(response_dict)
		context_dict['data'] = data
		context_dict['from_station'] = Station.objects.get(code=from_station)
		context_dict['to_station'] = Station.objects.get(code=to_station)
		context_dict['departure_date'] = date
		context_dict['departure_time'] = time
		context_dict['train_number'] = train_number
		context_dict['stations'] = Station.objects.all()
	return render(request, 'search/places.html', context_dict)
	
def passenger(request):
	context_dict = {}
	if request.method == 'POST':
		from_station = request.POST.get('from_station')
		to_station = request.POST.get('to_station')
		date = request.POST.get('departure_date')
		time = request.POST.get('departure_time')
		train_number = request.POST.get('train_number')
		car_number = request.POST.get('car_number')
		car_tariff = request.POST.get('car_tariff')
		car_type = request.POST.get('car_type')
		context_dict['from_station'] = Station.objects.get(code=from_station)
		context_dict['to_station'] = Station.objects.get(code=to_station)
		context_dict['departure_date'] = date
		context_dict['stations'] = Station.objects.all()
		context_dict['train_number'] = train_number
		context_dict['departure_time'] = time
		context_dict['car_number'] = car_number
		context_dict['car_tariff'] = car_tariff
		context_dict['car_type'] = car_type
	return render(request, 'search/passenger.html', context_dict)
	
def buy_ticket(request):
	context_dict = {}
	if request.method == 'POST':
		from_station = request.POST.get('from_station')
		to_station = request.POST.get('to_station')
		date = request.POST.get('departure_date')
		time = request.POST.get('departure_time')
		train_number = request.POST.get('train_number')
		car_number = request.POST.get('car_number')
		car_type = request.POST.get('car_type')
		doc_type = request.POST.get('doc_type')
		doc_number = request.POST.get('doc_number')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		middle_name = request.POST.get('middle_name')
		full_name = last_name+"="+first_name+"="+middle_name
		departure_date = datetime.strptime(date+" "+time, "%Y-%m-%d %H:%M")
		df = DateFormat(departure_date)
		client = Client(api_usernumber = conf.USER_NUMBER, api_passmd5 = conf.USER_PASSMD5, id_terminal = conf.ID_TERMINAL, id_service = conf.ID_SERVICE, request_url = conf.API_URL)
		class_service = ""
		if car_type==u"Люкс":
			class_service = u'1Л'
		elif car_type == u"Купе":
			class_service = u'2К'
		elif car_type == u"Плацкартный":
			class_service = u'3П'
		print car_type
		print class_service
		booking = client.buy_ticket(from_station, to_station, df.format('d.m.Y H:i'),  train_number, car_type, car_number, class_service, '0', '0', 'null', '1', 'null', 'null', doc_type, doc_number, full_name, car_type[0], '1')
		data = json.dumps(booking, ensure_ascii=False)
		response_dict = json.loads(data)
		if "GtETicket_Response" in response_dict:
			context_dict = handle_ticket(response_dict)
		else:
			context_dict['error'] = data
		context_dict['from_station'] = Station.objects.get(code=from_station)
		context_dict['to_station'] = Station.objects.get(code=to_station)
		context_dict['departure_date'] = date
		context_dict['stations'] = Station.objects.all()
	return render(request, 'search/ticket.html', context_dict)

def handle_ticket(info):
	context_dict = {}
	ticket = Ticket()
	order = info["GtETicket_Response"]["Order"]
	ticket.order_id = order["@ID"]
	ticket.express_id = order["@ExpressID"]
	departure = info["GtETicket_Response"]["Departure"]
	ticket.train = departure["@Train"]
	ticket.departure_date = departure["@Date"]
	ticket.departure_time = departure["@Time"]
	ticket.departure_station = departure["@Station"]
	arrival = info["GtETicket_Response"]["Arrival"]
	ticket.arrival_date = arrival["@Date"]
	ticket.arrival_time = arrival["@Time"]
	ticket.arrival_station = arrival["@Station"]
	car = info["GtETicket_Response"]["Car"]
	ticket.car_number = car["@Number"]
	ticket.car_type = car["@Type"]
	ticket.seat_number = info["GtETicket_Response"]["Seats"]["Seat"]
	ticket.price = info["GtETicket_Response"]["Tariff"]
	ticket.full_name = info["GtETicket_Response"]["Tickets"]["Ticket"]["Passenger"]["@Name"]
	ticket.save()
	context_dict['ticket'] = ticket
	return context_dict


def place_handler(info):
	context_dict = {}
	context_dict['from'] = info[u"Direction"][u"PassRoute"][u"@From"]
	context_dict['to'] = info[u"Direction"][u"PassRoute"][u"@To"]
	trains = info[u"Direction"][u"Trains"][u"Train"]
	if u"@Number" in trains:
		train_seat = TrainSeat()
		train_seat.number = trains[u"@Number"]
		train_seat.direction = trains[u"Route"][u"Station"][0] + " - " + trains[u"Route"][u"Station"][1]
		train_seat.departure_time = trains[u"Departure"][u"@Time"]
		train_seat.arrival_time = trains[u"Arrival"][u"@Time"]
		train_seat.duration = trains[u"TimeInWay"]
		context_dict['train_seat'] = train_seat
		context_dict['cars'] = parse_cars(trains[u"Cars"])
	else:
		for train in trains:
			train_seat = TrainSeat()
			train_seat.number = train[u"@Number"]
			train_seat.direction = train[u"Route"][u"Station"][0] + " - " + train[u"Route"][u"Station"][1]
			train_seat.departure_time = train[u"Departure"][u"@Time"]
			train_seat.arrival_time = train[u"Arrival"][u"@Time"]
			train_seat.duration = train[u"TimeInWay"]
			context_dict['train_seat'] = train_seat
			context_dict[ 'cars'] = parse_cars(train[u"Cars"])
	return context_dict
	
def parse_cars(info):
	cars = []
	if u"Car" in info:
		inf = info[u"Car"]
		if u"@Number" in inf:
			car = Car()
			car.number = inf[u"@Number"]
			car.car_type = info[u"@Type"]
			car.tariff = info["Tariff"]
			car.places = inf[u"Places"]
			cars.append(car)
		else:
			for i in inf:
				car = Car()
				car.number = i[u"@Number"]
				car.car_type = info[u"@Type"]
				car.tariff = info[u"Tariff"]
				car.places = i[u"Places"]
				cars.append(car)
	else:
		for elem in info:
			inf = elem[u"Car"]
			if u"@Number" in inf:
				car = Car()
				car.number = inf[u"@Number"]
				car.car_type = elem[u"@Type"]
				car.tariff = elem[u"Tariff"]
				car.places = inf[u"Places"]
				cars.append(car)
			else:
				for i in inf:
					car = Car()
					car.number = i[u"@Number"]
					car.car_type = elem["@Type"]
					car.tariff = elem[u"Tariff"]
					car.places = i[u"Places"]
					cars.append(car)
	return cars
		

def request_handler(info):
	context_dict = {}
	context_dict['from'] = info[u"Direction"][u"PassRoute"][u"@From"]
	context_dict['to'] = info[u"Direction"][u"PassRoute"][u"@To"]
	trains = info[u"Direction"][u"Trains"][u"Train"]
	train_seats = []
	if u"@Number" in trains:
		train_seat = TrainSeat()
		train_seat.number = trains[u"@Number"]
		train_seat.direction = trains[u"Route"][u"Station"][0] + " - " + trains[u"Route"][u"Station"][1]
		train_seat.departure_time = trains[u"Departure"][u"@Time"]
		train_seat.arrival_time = trains[u"Arrival"][u"@Time"]
		train_seat.duration = trains[u"TimeInWay"]
		cars = trains[u"Places"][u"Cars"]
		if u"@Type" in cars:
			count_available_seats(train_seat, cars)
		else:
			for car in cars:
				count_available_seats(train_seat, car)
		train_seats.append(train_seat)
	else:
		for train in trains:
			train_seat = TrainSeat()
			train_seat.number = train[u"@Number"]
			train_seat.direction = train[u"Route"][u"Station"][0] + " - " + train[u"Route"][u"Station"][1]
			train_seat.departure_time = train[u"Departure"][u"@Time"]
			train_seat.arrival_time = train[u"Arrival"][u"@Time"]
			train_seat.duration = train[u"TimeInWay"]
			cars = train[u"Places"][u"Cars"]
			if u"@Type" in cars:
				count_available_seats(train_seat, cars)
			else:
				for car in cars:
					count_available_seats(train_seat, car)
			train_seats.append(train_seat)
	context_dict['train_seats'] = train_seats
	return context_dict
	
def count_available_seats(train_seat, cars):
	tariffs = cars[u"Tariffs"][u"Tariff"]
	if u"Tariff" in tariffs:
		tariff = tariffs[u"Tariff"]
	else:
		tariff = tariffs[0][u"Tariff"]
	if cars[u"@IndexType"] == "1":
		train_seat.common_seats = cars["@FreeSeats"]
		train_seat.common_tariff = tariff
	if cars[u"@IndexType"] == "2":
		train_seat.sitting_seats = cars["@FreeSeats"]
		train_seat.sitting_tariff = tariff
	if cars[u"@IndexType"] == "3":
		train_seat.reserved_seats = cars["@FreeSeats"]
		train_seat.reserved_tariff = tariff
	if cars[u"@IndexType"] == "4":
		train_seat.compartment_seats = cars["@FreeSeats"]
		train_seat.compartment_tariff = tariff
	if cars[u"@IndexType"] == "5":
		train_seat.soft_seats = cars["@FreeSeats"]
		train_seat.soft_tariff = tariff
	if cars[u"@IndexType"] == "6":
		train_seat.luxury_seats = cars["@FreeSeats"]
		train_seat.luxury_tariff = tariff
	return train_seat
	


# Create your views here.
