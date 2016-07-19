# coding: utf-8

import dpath
import xmltodict


class BaseResponse(dict):
    _root_path = ''
    _force_list = ()

    def __init__(self, data, **kwargs):
        response = xmltodict.parse(data)
        self['response'] = data
        self['parsed'] = dpath.util.get(response, self._root_path)
        self['request'] = kwargs.pop('request', None)
        super(BaseResponse, self).__init__(response, **kwargs)


    def get_parsed(self):
        return self['parsed']


class RetrieveGuidResponse(BaseResponse):
    _root_path = 'request/body/idt/guid'

class SessionCloseResponse(BaseResponse):
    _root_path = 'request/body/status'

class PlacesResponse(BaseResponse):
    _root_path = 'request/body'

class TrainPlacesResponse(BaseResponse):
    _root_path = 'request/body'

class TicketResponse(BaseResponse):
    _root_path = 'request/body'

class ConfirmationResponse(BaseResponse):
    _root_path = 'request/body'