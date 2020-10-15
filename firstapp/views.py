from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

import requests

# Create your views here.
def index(request):
    return render(request, 'firstapp/index.html')

def newsearch(request):
    search = request.POST.get("search")                                         # Gets what the user typed in

    models.Search.objects.create(search = search)                               # Store the search in the database

    BASE_URL = "https://losangeles.craigslist.org/search/?query={}"             # Craigslist URL without the search parameter
    FINAL_URL = BASE_URL.format(quote_plus(search))                             # Craigslist URL with the search parameter

    response = requests.get(FINAL_URL)                                          # Response from the Craigslist website
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    results = soup.find_all('li', {'class': 'result-row'})
    # results_titles = results.find_all({'class': 'result-info'}).text          ### TRY THIS LATER. MIGHT WORK!
    # results_links = results.find_all('a').get('href')
    # results_prices = results.find_all({'class': 'result-price'}).text

    BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"
    final_results = []
    for result in results:
        title = result.find(class_='result-title').text
        link = result.find('a').get('href')
        if result.find(class_='result-price'):
            price = result.find(class_='result-price').text
        else:
            price = 'N/A'
        if result.find(class_='result-image').get('data-ids'):
            image_id = result.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            image_url = BASE_IMAGE_URL.format(image_id)
        else:
            image_url = "https://craigslist.org/images/peace.jpg"
        final_results.append((title, link, price, image_url))

    stuff_for_frontend = {
        'search': search,
        'final_results': final_results,
    }
    return render(request, 'firstapp/newsearch.html', stuff_for_frontend)
