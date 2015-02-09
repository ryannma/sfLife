from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django_ajax.decorators import ajax
from requests.auth import HTTPBasicAuth
import json
import requests
import logging
from . import form

logging.basicConfig()


def new(request):
    return render(request, 'dashboard.html')

@ajax
def watson(request):
    headers = {
        'content-type':'application/json'
    }
    #dict(queryDict.iterlists())
    #print request.body
    auth = HTTPBasicAuth('ec08b85d-cf22-46c5-b728-eec7f3f24c9a', '7zO3zKu73n3E')
    watson_url = 'https://gateway.watsonplatform.net/tradeoff-analytics-beta/api/v1/dilemmas'
    print request.body
    response = requests.post(watson_url, data=request.body, headers=headers, auth=auth)
    print response.content
    results = json.loads(response.text)
    return results