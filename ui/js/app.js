
$(document).on("click", "a", function () {
  var linkId = $(this).attr('id')
  if (linkId == 'meal') {
    $("#meal").addClass("green-txt-btn");
    $("#day").addClass("gray-txt-btn");
    $("#week").addClass("gray-txt-btn");
    localStorage.setItem('planfor', 'meal');
    getRecipes('vegetarian', 'meal')
  }
  if (linkId == 'day') {
    $("#meal").addClass("gray-txt-btn");
    $("#day").addClass("green-txt-btn");
    $("#week").addClass("gray-txt-btn");
    localStorage.setItem('planfor', 'day');
    getRecipes('vegetarian', 'day')
  }
  if (linkId == 'week') {
    $("#meal").addClass("gray-txt-btn");
    $("#day").addClass("gray-txt-btn");
    $("#week").addClass("green-txt-btn");
    localStorage.setItem('planfor', 'week');
    getRecipes('vegetarian', 'week')
  }
});

function getRecipes(diet, planMeal) {
  $.get("http://localhost:5000/api/v1.0?diet=" + diet + "&planfor=" + planMeal, function (data, status) {
    populateRecipes(data)
  });
}

function loadRecipes(diet, planMeal, mealTime, changeItem, mealPlan) {
  var planfor = localStorage.getItem('planfor')
  jsonPayload = { 'diet': diet, 'planfor': planfor, "day": planMeal, "mealtime": mealTime, "change_item": changeItem, "meal_plan": mealPlan }
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
  var diet = 'vegetarian'

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