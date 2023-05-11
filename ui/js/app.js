const veg = 'vegetarian'
const nonveg = 'nonvegetarian'
const meal = 'meal'
const day = 'day'
const week = 'week'
const selectedClass = 'selected';
const customRadius = 'custom-radius';

const planFor = 'planFor';
const breakfast = 'breakfast';
const lunch = 'lunch';
const dinner = 'dinner';
const singleMT = "singlemealtime";
$(document).on("click", "button", function () {
  var linkId = $(this).attr('id')
  var buttonClass = $(this).attr('class')
  var isVeg = localStorage.getItem('isVeg')
  if (linkId == veg) {
    if (buttonClass.includes(selectedClass)) {
      $(".meal-button").removeClass(customRadius);
      $(".meal-button").removeClass(selectedClass);
      let tmp = localStorage.getItem(planFor)
      $("#" + tmp).addClass(selectedClass);
      $("#" + tmp).addClass(customRadius);
      localStorage.setItem('isVeg', 'true');
      let mealtmp = localStorage.getItem(singleMT)
      getRecipes(veg, tmp, mealtmp)
    }
  }
  if (linkId == nonveg) {
    if (buttonClass.includes(selectedClass)) {
      let tmp = localStorage.getItem(planFor)
      $(".meal-button").removeClass(customRadius);
      $(".meal-button").removeClass(selectedClass);
      $("#" + tmp).addClass(selectedClass);
      $("#" + tmp).addClass(customRadius);
      localStorage.setItem('isVeg', 'false');
      let mealtmp = localStorage.getItem(singleMT)
      getRecipes(nonveg, tmp, mealtmp)
    }
  }
  if (linkId == meal) {
    localStorage.setItem(planFor, meal);
    $('#daymeal').removeClass('hide')
    $("#recipes").empty();
  }
  if (linkId == breakfast || linkId == lunch || linkId == dinner) {
    localStorage.setItem(singleMT, linkId);
    if (isVeg === 'true') {
      getRecipes(veg, meal, linkId)
    } else {
      getRecipes(nonveg, meal, linkId)
    }
  }
  if (linkId == day) {
    localStorage.setItem(planFor, day);
    $('#daymeal').addClass('hide')
    let tmp = localStorage.getItem(singleMT)
    if (isVeg === 'true') {
      getRecipes(veg, day, tmp)
    } else {
      getRecipes(nonveg, day, tmp)
    }
  }
  if (linkId == week) {
    localStorage.setItem(planFor, week);
    $('#daymeal').addClass('hide')
    let tmp = localStorage.getItem(singleMT)
    if (isVeg === 'true') {
      getRecipes(veg, week, tmp)
    } else {
      getRecipes(nonveg, week, tmp)
    }
  }
});

function getRecipes(diet, planMeal, mealTime) {
  $.get("http://localhost:5000/api/v1.0?diet=" + diet + "&planfor=" + planMeal + '&mealtime=' + mealTime, function (data, status) {
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