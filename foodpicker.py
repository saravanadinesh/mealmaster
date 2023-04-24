# ---------------------------------------------------------------------------------------------------------
# foodpicker.py
#   This is the main code of the mealmaster project. Functionalities such as picking a meal plan, altering -
#   it etc. are implemented here. 
# 
# ---------------------------------------------------------------------------------------------------------

import pandas as pd
import random
import json
from flask import Flask, request
app = Flask(__name__)

def pick_sidedish(maindish):
    dishesdb = pd.read_excel("Dishes_Database.xlsx", dtype=str).fillna("")
    maindishdf = dishesdb[(dishesdb["name"] == maindish)] # This should result in a single row dataframe
    if maindishdf.iloc[0]["sub type"] in ["Complete meal", "unspecified"]:
        return(None)

    if maindishdf.iloc[0]["only legitimate side dishes"] != "":
        sidedishes = maindishdf.iloc[0]["only legitimate side dishes"].split(", ")
        sidedish_name = random.choice(sidedishes)
    else:
        plan_done = False
        while plan_done == False:
            if maindishdf.iloc[0]["sub type"] == "pongal":
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "chutney")] 
            
            elif maindishdf.iloc[0]["sub type"] == "dhida-phalar": 
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "chutney")] 

            elif maindishdf.iloc[0]["sub type"] == "chapathi":
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "subzi")] 
            
            elif maindishdf.iloc[0]["sub type"] == "sambar":
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "ambad") |
                                        (dishesdb["sub type"] == "roast") |
                                        (dishesdb["sub type"] == "Vadai")] 
            
            elif maindishdf.iloc[0]["sub type"] == "pilchar":
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "poriyal") |
                                        (dishesdb["sub type"] == "kutkiri") |
                                        (dishesdb["sub type"] == "roast") |
                                        (dishesdb["sub type"] == "Vadai")] 
            
            elif maindishdf.iloc[0]["sub type"] == "omty":
                sidedishesdf = dishesdb[(dishesdb["sub type"] == "poriyal") |
                                        (dishesdb["sub type"] == "kutkiri") |
                                        (dishesdb["sub type"] == "roast") |
                                        (dishesdb["sub type"] == "Vadai")] 
            
            else:
                sidedishesdf = dishesdb[(dishesdb["type"] == "side dish")]
            
            sidedishesdf.reset_index(drop=True, inplace=True) 
            rowval = random.randint(0,sidedishesdf.shape[0]-1)
            sidedish_name = sidedishesdf.loc[rowval, "name"]

            # Make sure we haven't selected an illegitimate side dish
            bad_sidedishes = maindishdf.iloc[0]["illegitimate side dishes"].split(", ")
            if sidedish_name in bad_sidedishes:
                continue
            else:
                plan_done = True

    try:
        sidedish_dict = dishesdb[(dishesdb["name"] == sidedish_name)].iloc[0].to_dict()
    except:
        print("Exception")
    sidedish = {
                    "name": sidedish_dict["name"],
                    "type": "side dish", 
                    "sub type" : sidedish_dict["sub type"],
                    "dosha" : sidedish_dict["dosha"],
                    "anti dosha": sidedish_dict["anti dosha"]
               }

    return(sidedish) 


def plansinglemeal(diet, mealtime):    
    dishesdb = pd.read_excel("Dishes_Database.xlsx", dtype=str).fillna("")
    if mealtime == "breakfast":
        subdf = dishesdb[((dishesdb["time"] == "breakfast")
                        | (dishesdb["time"] == "breakfast or dinner"))
                        & (dishesdb["type"] == "main dish")
                        & (dishesdb["diet"] == diet)]
        no_of_maindishes = 1
    elif mealtime == "dinner":
        subdf = dishesdb[((dishesdb["time"] == "dinner")
                | (dishesdb["time"] == "breakfast or dinner")
                | (dishesdb["time"] == "lunch or dinner"))
                & (dishesdb["type"] == "main dish")
                & (dishesdb["diet"] == diet)]
        no_of_maindishes = 1
    else: # Assume mealtime is "lunch"
        subdf = dishesdb[((dishesdb["time"] == "lunch")
                        | (dishesdb["time"] == "lunch or dinner"))
                        & (dishesdb["type"] == "main dish")
                        & (dishesdb["diet"] == diet)]
        no_of_maindishes = 2

    subdf.reset_index(drop=True, inplace=True)
    items = []
    rowval = random.randint(0,subdf.shape[0]-1)
    maindish_name = subdf.loc[rowval, "name"]
    sidedish = pick_sidedish(maindish = maindish_name)
    if sidedish == None:
        items.append(
                    {
                        "name": maindish_name,
                        "type": "main dish",
                        "sub type" : subdf.loc[rowval, "sub type"],
                        "dosha" : subdf.loc[rowval, "dosha"],
                        "anti dosha": subdf.loc[rowval, "anti dosha"]
                    }
                )
    else:
        items.append({
                        "name": maindish_name,
                        "type": "main dish",
                        "sub type" : subdf.loc[rowval, "sub type"],
                        "dosha" : subdf.loc[rowval, "dosha"],
                        "anti dosha": subdf.loc[rowval, "anti dosha"]
                    })
        items.append({
                        "name": sidedish["name"],
                        "type": "side dish",
                        "sub type" : sidedish["sub type"],
                        "dosha" : sidedish["dosha"],
                        "anti dosha": sidedish["anti dosha"]
                    })

    if mealtime == "lunch":
        if items[0]["name"] != "Complete meal": # If we have chosen a complete meal already, then we are done
            if items[0]["sub type"] != "pilchar":
                subsubdf = subdf[(subdf["sub type"] == "pilchar") & (subdf["sub type"] != "Complete meal")]
            else:
                subsubdf = subdf[(subdf["sub type"] != "pilchar") & (subdf["sub type"] != "Complete meal")]

            subsubdf.reset_index(drop=True, inplace=True)
            rowval = random.randint(0,subsubdf.shape[0]-1)
            maindish_name = subsubdf.loc[rowval]["name"]

            plan_done = False
            while plan_done == False:
                sidedish = pick_sidedish(maindish = maindish_name)
                if len(items) > 1:  # Just an additional check to avoid weird bugs. Probably not needed
                    if sidedish["sub type"] == items[1]["sub type"]:
                        break
                    else:
                        plan_done = True
                else:
                    plan_done = True

            items.append({
                            "name": maindish_name,
                            "type": "main dish",
                            "sub type" : subsubdf.loc[rowval, "sub type"],
                            "dosha" : subsubdf.loc[rowval, "dosha"],
                            "anti dosha": subsubdf.loc[rowval, "anti dosha"]
                        })
            items.append({
                            "name": sidedish["name"],
                            "type": "side dish",
                            "sub type" : sidedish["sub type"],
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
#                       "sub type" : "pongal",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Vangi chutney",
#                       "type": "side dish",
#                       "sub type" : "chutney",
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
#                       "sub type" : "sambar",
#                       "dosha" : "vata",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Butter beans ambad",
#                       "type": "side dish",
#                       "sub type" : "ambad",
#                       "dosha" : "vata",
#                       "anti dosha": "unknown"
#                   },
#                   {
#                       "name": "Thikka pilchar",
#                       "type": "main dish",
#                       "sub type" : "pilchar",
#                       "dosha" : "",
#                       "anti dosha": ""
#                   },
#                   {
#                       "name": "Carrot muttakos poriyal",
#                       "type": "side dish",
#                       "sub type" : "poriyal",
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
@app.route('/api/v1.0')
def planmeals_api():
    args = request.args
    return planmeals(args.get("diet"), args.get("planfor"), args.get("mealtime"), args.get("request_type"), args.get("change_item"), args.get("meal_plan"))
def planmeals(diet="vegetarian", planfor="day", mealtime=None, request_type="new", change_item=None, meal_plan=None):
    if planfor == "meal":
        meal = plansinglemeal(diet = diet, mealtime = mealtime)
        mealplan = {"day":{"meal":meal}}

    elif planfor == "day":
        meal1 = plansinglemeal(diet = diet, mealtime = "breakfast")
        meal2 = plansinglemeal(diet = diet, mealtime = "lunch")
        
        plan_done = False   # This variable is used to tell us when to stop iterating on 
        while plan_done == False:
            meal3 = plansinglemeal(diet = diet, mealtime = "dinner")
            if meal1["items"][0]["sub type"] == meal3["items"][0]["sub type"]:  # Assuming items[0] will always be the main dish
                                                                                # We don't want two dishes of the same sub type,
                                                                                # ex. pongal, to be selected for both breakfast 
                                                                                # and dinner
                continue
            if len(meal1["items"]) == 2 and len(meal3["items"]) == 2 :
                if meal1["items"][1]["name"] == meal3["items"][1]["name"]:  # Assuming items[1] will always be the side dish
                                                                            # We don't want the same side dish for morning and night
                    continue
            
            plan_done = True
        
        mealplan = {"day":{"meal1":meal1, "meal2":meal2, "meal3":meal3}}

    else:   # Assume the plan request is for a week
        # Let us first select breakfast and dinner
        bf_subtypes = ["pongal", "pongal", "pongal", "dhida-phalar", "dhida-phalar", "dhida-phalar", "chapathi",
                       "chapathi", "Complete meal", "unspecified"]
        dinner_subtypes = ["pongal", "pongal", "dhida-phalar", "dhida-phalar", "dhida-phalar", "chapathi", "chapathi",
                           "Complete meal"]
       
        # Ensure breakfast items have enough diversity
        step_done = False        
        while step_done == False:
            bf_choices = random.choices(bf_subtypes, k=5)
            if bf_choices.count("pongal") > 3:
                continue
            elif bf_choices.count("dhida-phalar") > 3:
                continue
            elif bf_choices.count("chapati") > 2:
                continue
            else:
                step_done = True

        plan_done = False
        while plan_done == False:
            # Ensure dinner items have enough diversity
            step_done = False
            while step_done == False:
                dinner_choices = random.choices(dinner_subtypes, k=5)
                if dinner_choices.count("pongal") > 3:
                    continue
                elif dinner_choices.count("dhida-phalar") > 3:
                    continue
                elif dinner_choices.count("chapati") > 2:
                    continue
                else:
                    step_done = True
           
            # Check if there is enough diversity among breakfast and dinner items combined 
            temp_list = []
            temp_list.extend(bf_choices)
            temp_list.extend(dinner_choices)
            if temp_list.count("pongal") > 5:
                continue
            elif temp_list.count("dhida-phalar") > 5:
                continue
            elif temp_list.count("chapati") > 3:
                continue
            else:
                plan_done = True
            
        # Rearrange the dinner dishes so that we don't get two chapati meals on the same day, two pongals on the same day and so on
        no_of_tries = 5
        step_done = False
        tries = 0
        while (step_done == False and tries < no_of_tries):
            matches = 0
            for i in range(len(bf_choices)):
                if bf_choices[i] == dinner_choices[i]:
                    matches = matches + 1
                
            if (matches < 2):
                step_done = True
            else:
                random.shuffle(dinner_choices)
                tries = tries+1
                continue   
                
        # We are done with choosing breakfast and dinner. Lets choose lunch meals now.
        lunch_subtypes = ["omty", "omty", "omty", "sambar", "sambar", "sambar", "Complete meal"]    # omty and sambar will always be accompanied by 
                                                                                                    # a pilchar. 

        step_done = False
        while step_done == False:
            lunch_choices = random.choices(lunch_subtypes, k=5)
            # Ensure diversity of lunch items
            if lunch_choices.count("omty") > 3:
                continue
            elif lunch_choices.count("sambar") > 3:
                continue
            elif lunch_choices.count("Complete meal") > 2:
                continue
            else:
                step_done = True
    
        
        # Select main dishes for all meals
        dishesdb = pd.read_excel("Dishes_Database.xlsx", dtype=str).fillna("")
        bf_df = dishesdb[((dishesdb["time"] == "breakfast") 
                        | (dishesdb["time"] == "breakfast or dinner")) 
                        & (dishesdb["type"] == "main dish")
                        & (dishesdb["diet"] == diet)]
        dinner_df = dishesdb[((dishesdb["time"] == "dinner") 
                            | (dishesdb["time"] == "breakfast or dinner") 
                            | (dishesdb["time"] == "lunch or dinner")) 
                            & (dishesdb["type"] == "main dish")
                            & (dishesdb["diet"] == diet)]
        lunch_df = dishesdb[((dishesdb["time"] == "lunch") 
                            | (dishesdb["time"] == "lunch or dinner")) 
                            & (dishesdb["type"] == "main dish")
                            & (dishesdb["diet"] == diet)]
        
        
        # Choose actual breakfast dishes
        bf_dishes = []
        prev_bf_maindishes = []
        prev_bf_sidedishes = []
        for dishsubtype in bf_choices:
            subdf = bf_df[(bf_df["sub type"] == dishsubtype)]
            subdf.reset_index(drop=True, inplace=True) 
            
            maindish_chosen = False
            while maindish_chosen == False:
                rowval = random.randint(0, subdf.shape[0]-1)
                maindish = {
                            "name": subdf.loc[rowval, "name"],
                            "type": subdf.loc[rowval, "type"],
                            "sub type" : subdf.loc[rowval, "sub type"],
                            "dosha" : subdf.loc[rowval, "dosha"],
                            "anti dosha": subdf.loc[rowval, "anti dosha"]
                            }
                if maindish["name"] in prev_bf_maindishes:
                    continue 
                
                prev_bf_maindishes.append(maindish["name"])
                maindish_chosen = True

            sidedish_chosen = False
            while sidedish_chosen == False:
                sidedish = pick_sidedish(maindish["name"])
                if sidedish == None:
                    break
                if sidedish["name"] in prev_bf_sidedishes:
                    continue

                if sidedish != None:
                    prev_bf_sidedishes.append(sidedish["name"])
                sidedish_chosen = True
            if sidedish == None:
                bf_dishes.append([maindish,{}])
            else:
                bf_dishes.append([maindish, sidedish])

        # Choose actual dinner dishes
        dinner_dishes = []
        prev_dinner_maindishes = []
        prev_dinner_sidedishes = []
        for i, dishsubtype in enumerate(dinner_choices):
            subdf = dinner_df[(dinner_df["sub type"] == dishsubtype)]
            subdf.reset_index(drop=True, inplace=True) 
            
            maindish_chosen = False
            while maindish_chosen == False:
                rowval = random.randint(0, subdf.shape[0]-1)
                maindish = {
                            "name": subdf.loc[rowval, "name"],
                            "type": subdf.loc[rowval, "type"],
                            "sub type" : subdf.loc[rowval, "sub type"],
                            "dosha" : subdf.loc[rowval, "dosha"],
                            "anti dosha": subdf.loc[rowval, "anti dosha"]
                            }
                if maindish["name"] in prev_dinner_maindishes:
                    continue 
                
                prev_dinner_maindishes.append(maindish["name"])
                maindish_chosen = True

            sidedish_chosen = False
            while sidedish_chosen == False:
                sidedish = pick_sidedish(maindish["name"])
                if sidedish == None:
                    break
                if (sidedish["name"] in prev_dinner_sidedishes):
                    continue
                if bf_dishes[i][1] != {}:
                    if (sidedish["name"] == bf_dishes[i][1]["name"]):
                        continue

                if sidedish != None:
                    prev_dinner_sidedishes.append(sidedish["name"])
                sidedish_chosen = True

            if sidedish == None:
                dinner_dishes.append([maindish, {}])
            else:
                dinner_dishes.append([maindish, sidedish])

        # Choose actual lunch dishes
        lunch_dishes = []
        prev_lunch_maindishes = []
        prev_lunch_sidedishes = []
        for i, dishsubtype in enumerate(lunch_choices):
            subdf = lunch_df[(lunch_df["sub type"] == dishsubtype)]
            subdf.reset_index(drop=True, inplace=True) 
            
            maindish_chosen = False
            while maindish_chosen == False:
                rowval = random.randint(0, subdf.shape[0]-1)
                maindish = {
                            "name": subdf.loc[rowval, "name"],
                            "type": subdf.loc[rowval, "type"],
                            "sub type" : subdf.loc[rowval, "sub type"],
                            "dosha" : subdf.loc[rowval, "dosha"],
                            "anti dosha": subdf.loc[rowval, "anti dosha"]
                            }
                if (maindish["name"] in prev_lunch_maindishes) or (maindish["name"] in prev_dinner_maindishes):
                    continue 
                
                prev_lunch_maindishes.append(maindish["name"])
                maindish_chosen = True

            sidedish_chosen = False
            while sidedish_chosen == False:
                sidedish = pick_sidedish(maindish["name"])
                if sidedish == None:
                    break
                if (sidedish["name"] in prev_lunch_sidedishes):
                    continue

                if sidedish != None:
                    prev_lunch_sidedishes.append(sidedish["name"])
                sidedish_chosen = True

            if sidedish == None:
                lunch_dishes.append([maindish,{}])
            else:
                lunch_dishes.append([maindish, sidedish])
            
            if maindish["sub type"] in ["omty", "sambar"]:  # If the dish we just selected is an omty or a sambar, then we need
                                                            # a pilchar to accompany it
                subdf = lunch_df[(lunch_df["sub type"] == "pilchar")]
                subdf.reset_index(drop=True, inplace=True) 
                
                rowval = random.randint(0, subdf.shape[0]-1)
                maindish = {
                            "name": subdf.loc[rowval, "name"],
                            "type": subdf.loc[rowval, "type"],
                            "sub type" : subdf.loc[rowval, "sub type"],
                            "dosha" : subdf.loc[rowval, "dosha"],
                            "anti dosha": subdf.loc[rowval, "anti dosha"]
                            }
                
                sidedish_chosen = False # Now we have to choose a side dish for the pilchar
                while sidedish_chosen == False:
                    sidedish = pick_sidedish(maindish["name"])
                    
                    if sidedish == None:
                        break
                    if (sidedish["name"] in prev_lunch_sidedishes):
                        continue

                    if sidedish == None:
                        prev_lunch_sidedishes.append(sidedish["name"])
                    sidedish_chosen = True
                if sidedish == None:
                    lunch_dishes.append([maindish,{}])
                else:
                    lunch_dishes.append([maindish, sidedish])
            else:
                lunch_dishes.append([{}, {}])

        # Build the mealplan json from all the dishes selected in the above steps.
        days = []
        for day in range(5):
            meal1_items = bf_dishes[day]
            meal2_items = lunch_dishes[day*2]
            meal2_items.extend(lunch_dishes[day*2 + 1])
            meal3_items = dinner_dishes[day]

            days.append({
                            "meal1": {"time":"breakfast", "items": meal1_items},
                            "meal2": {"time":"lunch", "items": meal2_items},
                            "meal3": {"time":"dinner", "items": meal3_items}
                        })
        
        mealplan = {
                    "day1": days[0],
                    "day2": days[1],
                    "day3": days[2],
                    "day4": days[3],
                    "day5": days[4],
                    }


    return(mealplan)


# mealplan = planmeals(planfor="day")
# print(json.dumps(mealplan, indent=4))
if __name__ == '__main__':
    app.run()