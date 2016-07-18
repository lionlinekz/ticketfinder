from django.shortcuts import render
from django.http import HttpResponse
from models import Station

def index(request):
	stations = Station.objects.all()
	context_dict = {'stations': stations}
	return render(request, 'search/index.html', context_dict)

# Create your views here.
