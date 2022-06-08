from django.shortcuts import render


from rest_framework.response import Response

import requests
import environ
import mysql.connector




env = environ.Env()
# reading .env file
environ.Env.read_env()


# Create your views here.


def geoapi(request):

    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    # use api with your ip Address for retrieve geodata
    response = requests.get('http://ip-api.com/json/%s' % ip_address)
    geodata = response.json()
    lat = geodata['lat']
    lon = geodata['lon']
    API_KEY = env("API_KEY")
    # prepare url for display a map with api
    # API use api-key given by locationiq
    # API_KEY must be save in .env file at the root of the project (same as settings.py)
    # API_KEY=<YOUR_API_KEY> (without '')
    url = f"""https://maps.locationiq.com/v3/staticmap?key={API_KEY}&center={lat},{lon}&size=800x800&zoom=13&markers=size:small|color:red|{lat},{lon}"""

    return render(request, 'application/geoapi.html', {
        'ip': geodata['query'],
        'country': geodata['country'],
        'latitude': geodata['lat'],
        'longitude': geodata['lon'],
        'city': geodata['city'],
        'url': url
    })
    
def requestdb (request):
    conn = mysql.connector.connect(host="51.158.97.130",
                               user="lovelace", password="yGG6:q22iv", 
                               database="market_ranking",
                               port="9622",
                               use_unicode=True,
                               charset='utf8')
    cursor = conn.cursor()
# Opérations à réaliser sur la base ...

    cursor.execute("""SELECT *
                        FROM ranked_page r
                        INNER JOIN website w ON r.website_id = w.id
                        INNER JOIN keyword k ON k.id = r.keyword_id
                        WHERE k.keyword LIKE  '% Nutella %'
                    """, ())
    rows = cursor.fetchall()
    print(rows)
    conn.close()
    
    return render(request, 'application/requestdb.html', {
        'rows': rows})
        
        

