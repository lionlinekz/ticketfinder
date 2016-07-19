from client.client import Client
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateformat import DateFormat
from ticketfinder import settings as conf
from models import Station, TrainSeat
from datetime import datetime
import json



def index(request):
	stations = Station.objects.all()
	context_dict = {'stations': stations}
	return render(request, 'search/index.html', context_dict)
	
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
		context_dict['from_station'] = from_station
		context_dict['to_station'] = to_station
		context_dict['departure_date'] = date
		context_dict['stations'] = Station.objects.all()
	return render(request, 'search/trains.html', context_dict)
	
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
