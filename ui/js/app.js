const veg = 'veg'
const nonveg = 'nonveg'
const meal = meal
const day = 'day'
const selectedClass = selectedClass;
const customRadius = customRadius;

const planFor = planFor;
$(document).on("click", "button", function () {
  var linkId = $(this).attr('id')
  var buttonClass = $(this).attr('class')
  if(linkId ==veg) {
    if(!buttonClass.includes(selectedClass)) {
      $(".meal-button").removeClass(customRadius);
      $(".meal-button").removeClass(selectedClass);
      $("#day").addClass(selectedClass);
      $("#day").addClass(customRadius);
      localStorage.setItem(planFor, meal);
      localStorage.setItem('isVeg','true');
    }
  }
  if(linkId ==nonveg) {
    if(buttonClass.includes(selectedClass)) {
      $(".meal-button").removeClass(customRadius);
      $(".meal-button").removeClass(selectedClass);
      $("#day").addClass(selectedClass);
      $("#day").addClass(customRadius);
      localStorage.setItem(planFor, meal);
      localStorage.setItem('isVeg','false');
      getRecipes(nonveg, meal)
    }
  }
  if (linkId == meal) {
    localStorage.setItem(planFor, meal);
    var isVeg = localStorage.getItem('isVeg')
    if(isVeg === 'true') {
      getRecipes(veg, meal)
    } else {
      getRecipes(nonveg, meal)
    }
    
  }
  if (linkId == day) {
    localStorage.setItem(planFor, day);
    if(isVeg === 'true') {
      getRecipes(veg, day)
    } else {
      getRecipes(nonveg, day)
    }
  }
  if (linkId == week) {
    localStorage.setItem(planFor, week);
    if(isVeg === 'true') {
      getRecipes(veg, week)
    } else {
      getRecipes(nonveg, week)
    }
  }
});

function getRecipes(diet, planMeal) {
  $.get("http://localhost:5000/api/v1.0?diet=" + diet + "&planfor=" + planMeal, function (data, status) {
    populateRecipes(data)
  });
}

function loadRecipes(diet, planMeal, mealTime, changeItem, mealPlan) {
  var planfor = localStorage.getItem(planFor)
  jsonPayload = { 'diet': diet, planFor: planfor, "day": planMeal, "mealtime": mealTime, "change_item": changeItem, "meal_plan": mealPlan }
  console.log("Payload to be sent: ")
  console.log(JSON.stringify(jsonPayload))
  $.ajax({
    url: "http://localhost:5000/api/v1.0",
    type: "POST",
    data: JSON.stringify(jsonPayload),
    contentType: "application/json",
    dataType: "json",
    success: function (data, status, xhr) {
      populateRecipes(data)
    }
  });
}


function populateRecipes(data) {
  $("#recipes").empty();
  var requestJson = JSON.stringify(data);
  var jsonData = JSON.parse(requestJson);
  var diet = veg

  console.log(jsonData);
  for (const byDay in jsonData) {
    console.log("by day");
    console.log(byDay);
    console.log(jsonData[byDay]);
    var day = jsonData[byDay];

    $("#recipes").append('<h5 class="first-letter">' + byDay + '</h5>');
    for (const x in day) {
      console.log(day)
      var meal = day[x];
      console.log(meal)
      mealHeader = ''
      if (meal["time"] === null) {
        mealHeader = '<h6 class="first-letter">meal</h6>'
      } else {
        mealHeader = '<h6 class="first-letter">' + meal["time"] + '</h6>'
      }

      $("#recipes").append(mealHeader);

      var mealItems = meal["items"];
      console.log("mealItems");
      console.log(mealItems);
      var mealNames = '';
      localStorage.setItem("mealJson", requestJson);
      for (let i = 0; i < mealItems.length; i++) {
        if (typeof mealItems[i]["name"] !== 'undefined') {
          var divHtml =
            '<div class="card-panel recipe white row"><div class="recipe-details"><div class="recipe-title">' + mealItems[i]["name"] + '</div></div><div class="recipe-delete"><i class="material-icons cursor-pointer" id="refresh" data-id="' + mealItems[i]["name"] + '" data-json="' + requestJson.replace('\\"', '\'') + '" data-meal-day="' + byDay + '" data-meal-time="' + meal["time"] + '" data-diet="' + diet + '"">refresh</i></div></div>'
          $("#recipes").append(divHtml);
        }

      }
    }
  }
}