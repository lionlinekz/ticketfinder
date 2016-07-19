# coding: utf-8

import json
import logging
import requests as r
from os import path
from jinja2 import (Environment, FileSystemLoader)
from responses import RetrieveGuidResponse, SessionCloseResponse, PlacesResponse, TrainPlacesResponse, TicketResponse, ConfirmationResponse



loader = FileSystemLoader(path.join(path.dirname(__file__), 'templates'))
env = Environment(loader=loader)

logger = logging.getLogger(__name__)

CONNECTION_TIMEOUT = (15, 60)


class BaseRequest(dict):
    _template = ''
    _response_class = None
    _base_url = ''
    _url = ''
    _action = ''
    _data = {}

    def __init__(self, **kwargs):
        self['credentials'] = kwargs.pop('credentials', None)
        self['payload'] = kwargs.pop('payload', None)
        super(BaseRequest, self).__init__(**kwargs)

    def _log_file(self, filename, content, is_json=False):
        try:
            with open('logs/%s' % filename, 'w') as f:
                if is_json:
                    json.dump(content, f, default=decimal_default)
                else:
                    f.write(content)
        except:
            return 'Error writing %s' % filename

    def _request(self):
        request_kwargs = {
            'url': self['credentials']['request_url'] + self._url,
            'method': 'POST',
            'data': self._render_template(),
            'timeout': CONNECTION_TIMEOUT,
            'headers': {
                'Content-Type': 'application/xml; charset=utf-8',
            }
        }
        self._log_file('%s_req.xml' % self._template.replace('.xml', ''), request_kwargs['data'])
        try:
            response = r.request(**request_kwargs)
            #response = requests.post(self['credentials']['request_url'], data = self._render_template())
            response.raise_for_status()
            return response.text
        except Exception as e:
            print e
        return "exception"
        #self._log_file('%s_rsp.xml' % self._template.replace('.xml', ''), response.text)
        #logger.info(self._template,
        #            extra={'request': self['request'], 'response': response.text})
        

    def _render_template(self):
        template = env.get_template(self._template)
        context_dict = {}
        context_dict = self['credentials'].copy()
        if self['payload']:
            context_dict.update(self['payload'])
        self['request'] = template.render(context_dict).encode("utf-8")
        print self['request']
        return self['request']

    def render(self):
        return self._render_template()

    def run(self):
        response = self._request()
        return self._response_class(response, request=self['request']).get_parsed()


class AuthoriseRequest(BaseRequest):
    _template = 'authorisation.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = RetrieveGuidResponse


class CloseSessionRequest(BaseRequest):
    _template = 'close_session.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = SessionCloseResponse


class PlacesRequest(BaseRequest):
    _template = 'get_places.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = PlacesResponse


class TrainPlacesRequest(BaseRequest):
    _template = 'get_train_places.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = TrainPlacesResponse


class BuyTicketRequest(BaseRequest):
    _template = 'buy_ticket.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = TicketResponse

class PassengerList(BaseRequest):
    _template = 'passengers.xml'


class PayOrderRequest(BaseRequest):
    _template = 'pay_order.xml'
    _url = ''
    _action = 'http://gateway24.test.stel.kz/'
    _response_class = ConfirmationResponse

