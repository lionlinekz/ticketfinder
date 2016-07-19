# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from client import Client
import json

client = Client(api_usernumber = 1644, api_passmd5 = '098f6bcd4621d373cade4e832627b4f6', id_terminal = 1186, id_service = 2485, request_url = 'http://gateway24.test.stel.kz/')
auth = client.authorise()
print "authorised with guid key" + auth
#places = client.get_places('2708000', '2704600', '07.07.2016', '0123')

places = client.get_train_places('2708000', '2704600', '07.07.2016', '22:35', u'087Х')
print json.dumps(places, ensure_ascii=False)
book = client.buy_ticket('2708000', '2704600', '07.07.2016 22:35', u'087Х', u'Плацкартный', u'02', 
                    u'3П', '0', '1', 'null', '1',
                    'null', '007-007', u'УЛ', '019065153', u'Сарсенгалиев=Асет=Айтбаевич', 'П', '1')
print json.dumps(book, ensure_ascii=False)

close_session = client.close_session()
if close_session == '0':
	print "session closed"