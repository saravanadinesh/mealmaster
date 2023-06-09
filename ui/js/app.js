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
const domain = "localhost"


document.addEventListener('DOMContentLoaded', function () {
  var buttons = document.querySelectorAll('.my-button');

  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      buttons.forEach(function (btn) {
        btn.classList.remove('selected');
      });
      this.classList.add('selected');
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  var mealButtons = document.querySelectorAll('.meal-button');

  mealButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      mealButtons.forEach(function (btn) {
        btn.classList.remove('selected');
      });
      this.classList.add('selected');
    });
  });
});


document.addEventListener('DOMContentLoaded', function () {
  var mealButtons = document.querySelectorAll('.daymeal-button');

  mealButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      mealButtons.forEach(function (btn) {
        btn.classList.remove('selected');
      });
      this.classList.add('selected');
    });
  });
});



$(document).on("click", "button", function (event) {
  var linkId = $(this).attr('id')
  var buttonClass = $(this).attr('class')
  var isVeg = localStorage.getItem('isVeg')
  if (linkId == veg) {
    if (buttonClass.includes(selectedClass)) {
      let tmp = localStorage.getItem(planFor)
      localStorage.setItem('isVeg', 'true');
      let mealtmp = localStorage.getItem(singleMT)
      getRecipes(veg, tmp, mealtmp)
    }
  }
  if (linkId == nonveg) {
    if (buttonClass.includes(selectedClass)) {
      let tmp = localStorage.getItem(planFor)
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
  if (linkId == 'feedbacksubmit') {
    console.log("feedback submitted")

    event.preventDefault();

    // Get form input values
    var name = $('#name').val();
    var whatsappNumber = $('#Whatsappnumber').val();
    var email = $('#email').val();
    var feedback = $('#textarea1').val();

    // Validate email address
    if (email) {
      var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        // Display error message or perform appropriate action
        $('#feedbackmsg').text('Please enter a valid email address.');
        return; // Stop form submission
      }
    }

    if (whatsappNumber) {
      // Validate phone number (assuming 10-digit numeric format)
      var phoneNumberRegex = /^\d{10}$/;
      if (!phoneNumberRegex.test(whatsappNumber)) {
        // Display error message or perform appropriate action
        $('#feedbackmsg').text('Please enter a valid 10-digit phone number.');
        return; // Stop form submission
      }
    }

    var sessionID = $.cookie('session_id');
    // Perform AJAX request
    $.ajax({
      type: 'POST', // or 'GET' depending on your server-side handling
      url: 'http://' + domain + ':5000/api/v1.0/feedback', // Replace with your server-side script URL
      headers: {
        'X-Session-ID': sessionID
      },
      data: {
        name: name,
        whatsappNumber: whatsappNumber,
        email: email,
        feedback: feedback
      },
      success: function (response) {
        // Clear form fields
        $('#name').val('');
        $('#Whatsappnumber').val('');
        $('#email').val('');
        $('#textarea1').val('');

        // Display the response
        $('#feedbackmsg').text('Thanks for the feedback!'); // Replace with the appropriate element to show the response
        event.preventDefault();

        // You can also do further actions based on the response
      },
      error: function (xhr, status, error) {
        // Handle any errors that occur during the AJAX request
        console.error(error);
      }
    });
  }
});

function getRecipes(diet, planMeal, mealTime) {
  var session_id = $.cookie('session_id');
  $.get({
    url: "http://" + domain + ":5000/api/v1.0?diet=" + diet + "&planfor=" + planMeal + '&mealtime=' + mealTime,
    beforeSend: function (xhr) {
      var sessionID = session_id;
      xhr.setRequestHeader('X-Session-ID', sessionID);
    },
    success: function (data, status, jqXHR) {
      // Get all response headers as a string
      var headersString = jqXHR.getAllResponseHeaders();

      // Split the headers into individual lines
      var headersArray = headersString.trim().split(/[\r\n]+/);

      
      for (var i = 0; i < headersArray.length; i++) {
        var headerLine = headersArray[i];

        // Check if the line starts with "Set-Cookie:"
        if (/^Set-Cookie:/i.test(headerLine)) {
          var separatorIndex = headerLine.indexOf(':');
          var headerKey = headerLine.substr(0, separatorIndex).trim();
          var headerValue = headerLine.substr(separatorIndex + 1).trim();
    
          $.cookie(headerKey, headerValue, {
            expires: new Date('Tue, 30 May 2023 16:41:55 GMT'),
            path: '/'
          });
        }
      }
      
      populateRecipes(data)
    }
  });
}

function loadRecipes(diet, planMeal, mealTime, changeItem, mealPlan) {
  var planfor = localStorage.getItem(planFor)
  jsonPayload = { 'diet': diet, 'planfor': planfor, "day": planMeal, "mealtime": mealTime, "change_item": changeItem, "meal_plan": mealPlan }
  console.log("Payload to be sent: ")
  console.log(JSON.stringify(jsonPayload))
  var sessionID = $.cookie('session_id');
  $.ajax({
    url: "http://" + domain + ":5000/api/v1.0",
    type: "POST",
    data: JSON.stringify(jsonPayload),
    contentType: "application/json",
    dataType: "json",
    headers: {
      'X-Session-ID': sessionID
    },
    success: function (data, status, jqXHR) {
      // Get all response headers as a string
      var headersString = jqXHR.getAllResponseHeaders();

      // Split the headers into individual lines
      var headersArray = headersString.trim().split(/[\r\n]+/);

      
      for (var i = 0; i < headersArray.length; i++) {
        var headerLine = headersArray[i];

        // Check if the line starts with "Set-Cookie:"
        if (/^Set-Cookie:/i.test(headerLine)) {
          var separatorIndex = headerLine.indexOf(':');
          var headerKey = headerLine.substr(0, separatorIndex).trim();
          var headerValue = headerLine.substr(separatorIndex + 1).trim();
    
          $.cookie(headerKey, headerValue, {
            expires: new Date('Tue, 30 May 2023 16:41:55 GMT'),
            path: '/'
          });
        }
      }
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