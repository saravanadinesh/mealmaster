# nutrition_facts.py -----------------------------------------------------------------------
#   Fetches nutrition facts from FoodData central (USDA), parses the data and displays in a  
# easily readable format
# ------------------------------------------------------------------------------------------
import pandas as pd
import requests
import json
import os

def get_nutrition_facts(foodname = None):
    #Create a default response
    response = {    'result':"failure", 
                    'reason for failure': "not set", 
                    'facts': None}  # Setting the result to "success" must be a deliberate 
                                    # act. This saves us from unnecessary bugs           
                                   
    # Global parameters
    FDC_URL = "https://api.nal.usda.gov/fdc/v1/foods"
    FDC_KEY = os.environ.get('FDC_API_KEY')
    
    # Search for the food in the database
    URL_SUFFIX = "/search"
    json_data = {   "query": foodname,
                    "dataType": ["Survey (FNDDS)"], 
                    "sortBy": "dataType.keyword", 
                    "sortOrder": "desc",
                    "numberOfResultsPerPage":1, 
                    "pageSize":1, 
                    "requireAllWords":True}
    headers = {
    'Content-Type': 'application/json',
    }
    
    params = {
        'api_key': FDC_KEY,
    }
    

    req_response = requests.post('https://api.nal.usda.gov/fdc/v1/foods/search', params=params, headers=headers, json=json_data)
    try:
        food = req_response.json()['foods'][0] 
    except:
        response.reason_for_failure = "Something wrong with the request response"
        return(response)
    
    # Test code
    # for nutrient in food['foodNutrients']:
    #     tabs = "\t"*nutrient['indentLevel']
    #     print(tabs+nutrient['nutrientName'], "\t", nutrient['value'], " ", nutrient['unitName'])

    # Copy relevant nutrient info into another dictionary (Because we don't really need all the info related to nutrients
    food_nutrients = []
    for nutrient in food['foodNutrients']:
        food_nutrients.append({ 'nutrient name':nutrient['nutrientName'], 
                                'value':nutrient['value'],
                                'unit':nutrient['unitName']}) 

    response['result'] = "Success"
    
    response['facts'] = {   'description':food['description'],
                            'fdcid': food['fdcId'],
                            'score': food['score'],
                            'gram_weight':food['finalFoodInputFoods'][0]['gramWeight'],
                            'food nutrients': food_nutrients} 
    print("Number of nutrients: ", len(req_response.json()['foods'][0]['foodNutrients']))
    return(response)
