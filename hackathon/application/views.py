from django.shortcuts import render


from rest_framework.response import Response

import aiohttp
import asyncio

import environ
import mysql.connector
from mysql.connector import errorcode




env = environ.Env()
# reading .env file
environ.Env.read_env()


# Link nutriscore to image url of nutriscore
def nutriscoreUrl(nutriscoreResult) :
    nutriscoreUrl=""
    nutriscoreImageUrl = {
    "scoreA" : "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Nutri-score-A.svg/240px-Nutri-score-A.svg.png",
    "scoreB" : "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nutri-score-B.svg/240px-Nutri-score-B.svg.png",
    "scoreC" : "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Nutri-score-C.svg/240px-Nutri-score-C.svg.png",
    "scoreD" : "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Nutri-score-D.svg/240px-Nutri-score-D.svg.png",
    "scoreE" : "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Nutri-score-E.svg/240px-Nutri-score-E.svg.png",
    }
    if nutriscoreResult == "a" :
        nutriscoreUrl = nutriscoreImageUrl['scoreA']
    elif nutriscoreResult == "b" :
        nutriscoreUrl = nutriscoreImageUrl['scoreB']
    elif nutriscoreResult == "c" :
        nutriscoreUrl = nutriscoreImageUrl['scoreC']
    elif nutriscoreResult == "d" :
        nutriscoreUrl = nutriscoreImageUrl['scoreD']
    elif nutriscoreResult == "e" :
        nutriscoreUrl = nutriscoreImageUrl['scoreE']
    return (nutriscoreUrl)
        

# Fetch API openfoodfacts.org with keywords to obtain list of products which matching with these keywords
def fetchApi(request):
    keywords = ''
    productList = []
    productKeywords = ''
    productImageUrl = ''
    productNutriscoreUrl = ''
    productName = ''
    productsInfo = []
    
    async def get_products():
        try :
            async with aiohttp.ClientSession() as session:
                apiUrl = f"""https://fr.openfoodfacts.org/cgi/search.pl?search_terms={keywords}&search_simple=1&action=process&json=1"""
                async with session.get(apiUrl) as response:
                    products = await response.json()
        except Exception as e:
            print(e)
            raise
        return products['products']
    if request.POST:
        keywords = request.POST.get("keywords")
        productList = asyncio.run(get_products())
        if len(productList) :
           
            for product in productList :
                if 'image_front_small_url' in product:
                    productImageUrl = product['image_front_small_url']
                else:
                    productImageUrl = ''
                if 'product_name_fr' in product :
                    productName = product['product_name_fr']
                else :
                    productName = product['product_name']
                if 'nutriscore_grade' in product:
                    nutriscoreResult = product['nutriscore_grade']
                    productNutriscoreUrl = nutriscoreUrl(nutriscoreResult)
                else:
                    productNutriscoreUrl = ''
                productKeywords = product['product_name'].split(" ")
                productsInfo .append({'productKeywords': productKeywords,
                                'productName': productName,
                                'productImageUrl' : productImageUrl,
                                'productNutriscoreUrl': productNutriscoreUrl})
                                                                                            
           
    return {
    'productsInfo': productsInfo,
    'keywords' : keywords,
    }
    
# Request on a private db with an array of keywords product to get the ranking of stores (Auchan, Carrefour) for a google search which uses these keywords
# TO DO: keywords array must contain 4 elements / if <4 add '' to complete array
def requestdb (keywords):
    rows = []
    DATABASE_PASSWORD = env("DATABASE_PASSWORD")
    connect = mysql.connector.connect(host="51.158.97.130",
                               user="lovelace",
                               password=DATABASE_PASSWORD, 
                               database="market_ranking",
                               port="9622",
                               use_unicode=True,
                               charset='utf8')
    cursor = connect.cursor()
    
    
    
# Opérations à réaliser sur la base ... 
    
    try:
        query = ("SELECT domain_name, SUM(visibility_score) s"
                "FROM ranked_page r"
                "INNER JOIN website w ON r.website_id = w.id"
                "INNER JOIN keyword k ON k.id = r.keyword_id"
                "WHERE k.keyword LIKE %s"
                "AND k.keyword LIKE %s"
                "AND k.keyword LIKE %s"
                "AND k.keyword LIKE %s"
                "GROUP by website_id"
                "ORDER BY s DESC"
                )
        cursor.execute(query, (keywords[0], keywords[1], keywords[2], keywords[3]))
        rows = cursor.fetchall()
        print(rows)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)    
    else:
        connect.close()
    
    return {'rows': rows}
    
    
def index (request) :
    context = fetchApi(request)
    # TO DO: Add requestdb(keywords) with keywords = name product  of a product of products list
           
    return render(request, 'application/index.html', context)
   
        
