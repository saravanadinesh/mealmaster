
$(document).on("click", "a", function(){
    var linkId = $(this).attr('id')
    if(linkId == 'single') {
        $("#single").addClass("green-txt-btn");
        $("#day").addClass("gray-txt-btn");
        $("#week").addClass("gray-txt-btn");
        loadRecipes('meal');
    }
    if(linkId == 'day') {
        $("#single").addClass("gray-txt-btn");
        $("#day").addClass("green-txt-btn");
        $("#week").addClass("gray-txt-btn");
        loadRecipes('day');
    }
    if(linkId == 'week') {
        $("#single").addClass("gray-txt-btn");
        $("#day").addClass("gray-txt-btn");
        $("#week").addClass("green-txt-btn");
        loadRecipes('week');
    }
});

function loadRecipes(planMeal) {
    $.get("http://localhost:5000/api/v1.0?diet=vegetarian&planfor=" + planMeal, function (data, status) {
    $("#recipes").empty();
    

    requestJson = JSON.stringify(data);
    var jsonData = JSON.parse(requestJson);

    console.log(jsonData);
    for (const byDay in jsonData) {
      console.log("by day");
      console.log(byDay);
      console.log(jsonData[byDay]);
      var day = jsonData[byDay];

      $("#recipes").append('<h2 class="first-letter">' + byDay + '</h2>');
      for (const x in day) {
        console.log(day)
        var meal = day[x];
        console.log(meal)
        mealHeader = ''
        if(meal["time"] === null) {
            mealHeader = '<h3 class="first-letter">meal</h3>'
        } else {
            mealHeader = '<h3 class="first-letter">' + meal["time"] + '</h3>'
        }
        
        $("#recipes").append(mealHeader);

        var mealItems = meal["items"];
        console.log("mealItems");
        console.log(mealItems);
        var mealNames = '';
        for (let i = 0; i < mealItems.length; i++) {
          if (typeof mealItems[i]["name"] !== 'undefined') {
            var divHtml =
              '<div class="card-panel recipe white row"><div class="recipe-details"><div class="recipe-title">' + mealItems[i]["name"] + '</div></div><div class="recipe-delete"><i class="material-icons" id="refresh" link="http://localhost:5500/api/v1.0?time=meal["time"]" data-id="'+ mealItems[i]["name"] +'" data-json="' + requestJson + '>refresh</i></div></div>'
            $("#recipes").append(divHtml);
          }

        }
      }
    }
  });
}