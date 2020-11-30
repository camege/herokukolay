from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import requests
import json
import os

#
#TOKEN = "SCXbnAgPMbDBTbbzUfCZ2RA7D7qQ4rnaQuqqECNP"

class Person:
  def __init__(self,id, name, surname):
    self.id = id
    self.name = name
    self.surname = surname
  allUnits = []
  
def getOthers(person_list, TOKEN):

    for person in person_list:

        url = "https://kolayik.com/api/v2/person/view/" + person.id

        payload = {}
        headers= {'Authorization':TOKEN}
        response = requests.request("GET", url, headers=headers, data = payload)
        
        json_data = json.loads(response.text)
#        print(json_data['data']['person']['unitList'][0]['items'])
        person.allUnits = json_data['data']['person']['unitList'][0]['items']
    return person_list

# Create your views here.
def index(request):
    person_list = []
    
    TOKEN = request.GET.get('token')
    
    url = "https://kolayik.com/api/v2/person/list"

    payload = {'status': 'active'}
    headers= {'Authorization':TOKEN}

    response = requests.request("POST", url, headers=headers, data = payload)
        
    json_data = json.loads(response.text)

    for item in json_data['data']['items']:
        p1 = Person(item['id'],item['firstName'], item['lastName'])
        person_list.append(p1)
    
#    return HttpResponse('<pre>' + response.text + '</pre>')

    person_list = getOthers(person_list, TOKEN)
    
    print(request.GET.get('token'))
    
    if request.method == "POST":
        return HttpResponseRedirect(reverse("hello:url"))
    else:
        return render(request, 'index.html', {'person_list':person_list})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
