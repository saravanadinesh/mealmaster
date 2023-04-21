# ---------------------------------------------------------------------------------------------------------
# foodpicker.py
#   This is the main code of the mealmaster project. Functionalities such as picking a meal plan, altering -
#   it etc. are implemented here. 
# 
# ---------------------------------------------------------------------------------------------------------

import pandas as pd
from random import randint

def plansinglemeal(diet, mealtime)    
    dishesdb = pd.read_excel("Dishes_Database.xlsx", dtype=str).fillna("")
    while plan_done == False:
        if planfor == "meal":
            if mealtime == "breakfast":
                subdf = dishesdb[((dishesdb["time"] == "breakfast") 
                                | (dishesdb["time"] == "breakfast or dinner")) 
                                & (dishesdb["type"] == "main dish")
                                & (dishesdb["diet"] == diet]
                no_of_maindishes = 1
            elif mealtime == "dinner":
                subdf = dishesdb[((dishesdb["time"] == "dinner") 
                        | (dishesdb["time"] == "breakfast or dinner") 
                        | (dishesdb["time"] == "lunch or dinner")) 
                        & (dishesdb["type"] == "main dish")
                        & (dishesdb["diet"] == diet]
                no_of_maindishes = 1
            else: # Assume mealtime is "lunch"
                subdf = dishesdb[((dishesdb["time"] == "lunch") 
                                | (dishesdb["time"] == "lunch or dinner")) 
                                & (dishesdb["type"] == "main dish")
                                & (dishesdb["diet"] == diet]
                no_of_maindishes = 2 
            
            items = []        
            for i = range(no_of_maindishes):    
                rowval = randint(0,subdf.shape[0])
                maindish_name = subdf.loc[rowval, "name"]
                sidedish = pick_sidedish(maindish = maindishname)
                if sidedish_name == None:
                    items.append = (    
                                {
                                    "name": maindish_name,
                                    "type": "main dish", 
                                    "subtype" : subdf.loc[rowval, "subtype"],
                                    "dosha" : subdf.loc[rowval, "dosha"],
                                    "anti dosha": subdf.loc[rowval, "anti dosha"]
                                }
                            )
                else:
                    items.append({
                                    "name": maindish_name,
                                    "type": "main dish", 
                                    "subtype" : subdf.loc[rowval, "subtype"],
                                    "dosha" : subdf.loc[rowval, "dosha"],
                                    "anti dosha": subdf.loc[rowval, "anti dosha"]
                                })
                    items.append({
                                    "name": sidedish["name"],
                                    "type": "side dish", 
                                    "subtype" : sidedish["subtype"],
                                    "dosha" : sidedish["dosha"],
                                    "anti dosha": sidedish["anti dosha"]
                                })
                
            meal = { 
                    "time":mealtime,
                    "items":items
                   }
            
            return(meal)         



# planmeals-------------------------------------------------------------------------------------------------------  
# Creates a meal plan based on dietary preferences of the user and how many meals he wishes the software to plan
# for.
#
# Arguments:
#   1. diet*: "vegetarian" or "nonvegetarian" 
#   2. planfor: "meal" or "day" or "week"
#   3. mealtime: "breakfast" or "lunch" or "dinner" or None. This cannot be set to None if "planfor" variable is
#                "meal"
#   4. request_type*: "new" or "change"
#   5. change_item: A string mentioning which item needs to be changed. Ex: "day1, meal2, Yellow poosani sambar"
#                   This argument is mandatory only if request_type is set to "change"
#   6. mealplan: The original mealplan json. This argument is mandatory only if request_type is set to "change"  
#
# Return value:
#
#   mealplan: A json variable as described below (with an example).
#   {
#       "day1": {
#           "meal1": {
#               "time": "breakfast",
#               "items": [
#                   {
#                       "name": "Mudha pongal",
#                       "type": "main dish", 
#                       "subtype" : "pongal",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Vangi chutney",
#                       "type": "side dish",
#                       "subtype" : "chutney",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   }
#               ]
#           }
#           "meal2": {
#               "time": "lunch", 
#               "items": [
#                   {
#                       "name": "Yellow poosani sambar",
#                       "type": "main dish",
#                       "subtype" : "sambar",
#                       "dosha" : "vata",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Butter beans ambad",
#                       "type": "side dish",
#                       "subtype" : "ambad",
#                       "dosha" : "vata",
#                       "anti dosha": "unknown"
#                   },
#                   {
#                       "name": "Thikka pilchar",
#                       "type": "main dish",
#                       "subtype" : "pilchar",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Carrot muttakos poriyal",
#                       "type": "side dish",
#                       "subtype" : "poriyal",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   },
#               ]
#           }
#           "meal3": {...},
#           "meal4": {...}
#       },
#   day2: {...},
#   day3: {...}
#   }
#
# Implementation methodology:
#   Since food we eat are associated with human preferences, which to some level is not based on logic, no 
# conventional computer program can produce a meal plan that is flawless from a human's perspective. For ex. We
# might like eating pongal and some variety rices with sambar and chutney, but some others with raita. There are 
# many such unwritten rules. If we try to implement them all in a conventional computer program, the code will 
# become intractable. Instead, we will try to implement some high level rules and then let the users tell us -
# either explicitly by clicking a button in the app that says, "I like this plan" or implicitly when they use the
# retry icon to ask for an alternative suggestion - what combinations of main dishes and side dishes work, or at 
# a higher level, what combinations of breakfast, lunch, dinner work. We will collect the user data and use AI to
# make our suggestions better. For now, this function implements only non AI part - i.e., the part that uses some
# high level food-picking rules. Furthermore, it will only consider the rules for a Tamil audience (in the interest
# of taking it quickly to the market).
#
#   We will use a database called "Dishes_Database" which contains some 200 food items along with their 
# attributes such as whether it is a breakfast/lunch/dinner item, its type (pongal chutney, complete meal etc.), 
# and more.   
#   
#   If the user asks us to give him/her a suggestion for a single meal, we will simply pick randomly an item
# suitable for the time of the day and ensure that the main dish - side dish combinations are legitimate based on 
# some global rules (don't combine chapathi with chutneys, omty with ambads etc.) and also information about
# legitimate combinations explicitly mentioned in the database. 
#
#   If the user asks us to suggests meals for the whole day, we will use the same logic as in the paragrah above,
# but also ensure that we don't accidentally pick the same meal for, say, breakfast and dinner.
#
#   If we are tasked with picking meals for an entire week (5 days), we will use the logic we used in the above two
# paragraphs but additionally, we will use the following:
#       1. We assume that idlis and dosas are quintessial to a Tamil diet. So we will ensure that there is at least
#       one idli and two dosas among a week's breakfasts and dinners taken together. We can do this by simply choosing
#       three slots randomly in breakfasts,dinners and reserving them for one idli means and two dosa meals.
#       2. We have to ensure that idli always comes before dosas. There are reasons why this isn't necessarily the 
#       right choice: People may start with the previous week's batter and make dosas and make a new batter for idli
#       later on. However, we will assume that this is an exception and ignore it. It makes the code simpler. 
#       Furthermore, the user can always use the retry symbol to change the dishes if he/she wishes. So it is not a
#       big deal. 
#        
# --------------------------------------------------------------------------------------------------------------- 
def planmeals(diet="vegetarian", planfor="day", mealtime=None, request_type="new", change_item=None, meal_plan=None):
    if planfor == "meal":
        meal1 = plansinglemean(diet = diet, mealtime = mealtime)
    elif planfor == "day":
        meal1 = plansinglemean(diet = diet, mealtime = "breakfast")
        meal2 = plansinglemean(diet = diet, mealtime = "lunch")
        
        plan_done = False   # This variable is used to tell us when to stop iterating on 
        while plan_done = False: 
            meal3 = plansinglemean(diet = diet, mealtime = "dinner")
            if meal1["items"][0]["subtype"] == meal3["items"][0]["subtype"]:    # Assuming items[0] will always be the main dish
                                                                            # We don't want two dishes of the same subtype,
                                                                            # ex. pongal, to be selected for both breakfast 
                                                                            # and dinner
                continue
            if len(meal1[items]) == 2 and len(meal3[items]) == 2 :
                if meal1["items"][1]["name"] == meal3["items"][1]["name"]:  # Assuming items[1] will always be the side dish
                                                                            # We don't want the same side dish for morning and night
                    continue
            
            plan_done = True
 

                
            
            
