from django.shortcuts import render


from rest_framework.response import Response

import requests
import environ
import mysql.connector




env = environ.Env()
# reading .env file
environ.Env.read_env()


# Create your views here.


def fetchApi(request):

    url = f"""https://fr.openfoodfacts.org/cgi/search.pl?search_terms=pate+a+tartiner&search_simple=1&action=process&json=1"""
    response = requests.get(url)
    response= response.json()
    productList = response['products']
    productKeywords = []
    productKeywordsList = []
    for product in productList :
        productKeywords = product['product_name_fr'].split(" ")
        productKeywordsList.append(productKeywords[0])
   
    return render(request, 'application/fetchApi.html', {
        'productKeywordsList': productKeywordsList,
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
        
        

