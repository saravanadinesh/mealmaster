# nutrition_facts.py -----------------------------------------------------------------------
#   Fetches nutrition facts from FoodData central (USDA), parses the data and displays in a  
# easily readable format
# ------------------------------------------------------------------------------------------
import pandas as pd
import requests
import json
import os

def get_nutrition_facts(food_name = None, fdc_id=None):
    #Create a default response
    response = {    'result':"failure", 
                    'reason for failure': "not set", 
                    'facts': None}  # Setting the result to "success" must be a deliberate 
                                    # act. This saves us from unnecessary bugs           
                                   
    # Global parameters
    FDC_KEY = os.environ.get('FDC_API_KEY')
    if fdc_id != None:
        # Get the food from the database using the exact FDC ID
        FDC_URL = "https://api.nal.usda.gov/fdc/v1/food/"+str(fdc_id)

        params = {
            'api_key': FDC_KEY,
        }
        
        # Make the request to the FSDA database
        req_response = requests.get(FDC_URL, params=params)
        
        try:
            food = req_response.json() 
        except:
            response.reason_for_failure = "Something wrong with the request response"
            return(response)
        
        ## Test code
        #print("Response:")
        #for nutrient in req_response.json()['foodNutrients']:
        #    try:
        #        print(nutrient['nutrient']['name'], " ", nutrient['nutrient']['number'], " ",nutrient['amount'], " ",nutrient['nutrient']['unitName']) 
        #    except:
        #        continue

        response['result'] = "Success"
        
        food_nutrients = []
        for nutrient in food['foodNutrients']:
            try:
                food_nutrients.append({ 'nutrient name':nutrient['nutrient']['name'], 
                                        'value':nutrient['amount'],
                                        'unit':nutrient['nutrient']['unitName']}) 
            except: # We do this because for some foods the first array element doesn't seem to be a nutrient
                continue 
            
        response['facts'] = {   'description':food['description'],
                                'fdcid': food['fdcId'],
                                'score': None, # Only /foods/search endpoint returns score. '/food' endpoint doesn't return it
                                'gram_weight':'100', # This seems to be hardcoded for GET requests in FDC database
                                'food nutrients': food_nutrients} 
        
    else:
        # Search for the food in the database
        FDC_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
        json_data = {   "query": food_name,
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
        
        # Make the request to the FSDA database
        req_response = requests.post(FDC_URL, params=params, headers=headers, json=json_data)
        try:
            food = req_response.json()['foods'][0] 
        except:
            response.reason_for_failure = "Something wrong with the request response"
            return(response)
        
        ##Test code
        #for nutrient in food['foodNutrients']:
        #    tabs = "\t"*nutrient['indentLevel']
        #    #print(tabs+nutrient['nutrientName'], "\t", nutrient['value'], " ", nutrient['unitName'])
        #    print(nutrient['nutrientName'], "\t", nutrient['value'], " ", nutrient['unitName'])

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
