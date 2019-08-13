// #region AJAX send the SIGNUP data to Flask/Python
  $('#signupForm').submit(function (event) {
    event.preventDefault();
    // ensure passwords match
    if ($('#signupPassword').val() == $('#confirmPassword').val()) {
      $.ajax({
        url: '/signup_user',
        data: $('#signupForm').serialize(),
        type: 'POST',
        success: function (response) {
          if (response == "success") {
            var message = "Your account was created. You can log in now.";
            $("#signupMessages").html(message);
            var delay = 1000;
            setTimeout(function () { window.location.href = "/"; }, delay);
          }
          else if (response == "fail") {
            var messagefail = "This username has already been registered.";
            $("#signupMessages").html(messagefail);
          }
        },
        error: function (error) {
          $("#signupMessages").html("There was an error creating your account. Please try again.");
        }
      });
    } else
      $('#signupMessages').html('Passwords do not match').css('color', 'red');
  });



  // #region AJAX RATE THIS RECIPE


  $('#rateme').click(function (e) {
    e.preventDefault();
    addVote();
    return false; //return false;  stops page jumping back to top
  });
  function addVote() {
    votes = 1;
    var url = window.location.href;
    recipe_id = url.split("/").pop();
    $.ajax({
      url:  + recipe_id,
      contentType: 'application/json',
      data: JSON.stringify(votes),
      type: 'POST',
      success: function (response) {
        if (response == 'fail') {
          $("#ratemeMessages").html("You have already voted for this recipe");
        }
        else {
          $("#vote_result").html(response);
        }
      },
      error: function (error) {
        $("#ratemeMessages").html("There was an error rating the recipe. Please try again.");
      }
    });
  }
  // #endregion

// #region AJAX Login data message send to Python/Flask


 $('#loginForm').submit(function(e){
      e.preventDefault();
      $.ajax({
        url: '/login_user',
        data: $('#loginForm').serialize(),
        type: 'POST',
        success: function (response) {
          if (response == 1) {
            $("#wrongusernameorpassword").html("Wrong password");
          }
          else if (response == 2) {
            $("#wrongusernameorpassword").html("Wrong Username");
          }
          else {
            $("#wrongusernameorpassword").html(response.message);
            //Add username and id to localstorage
            localStorage.setItem("username", response.username);
            localStorage.setItem("user_id", response._id);
            var delay = 1200;
            setTimeout(function () { window.location.href = "/myrecipes?limit=5&offset=0"; }, delay);
            }
        },
        error: function (error) {
          $("#wrongusernameorpassword").html("Please try again. There was an error logging in. ");
      }
    });
  });

  
  // #endregion

  // #region GET CATEGORY FROM SEARCH FILTER AND PASS TO FLASK


    $("#category-select").change(function (event) {
      event.preventDefault();
      var categorypicked = $('#category-select').find(":selected").text();
      var category = categorypicked.trim();
      $.ajax({
        url: '/filter_by_category/' + category,
        contentType: 'application/json',
        data: JSON.stringify(category),
        type: 'POST',
        success: function (response) {
          $("#searchResult").show();
          $("h3.section-subheading").html("Recipes searched by Category: " + categorypicked);
          $('#category-select').val("Select a Category");
          if (response != "fail") {
            $("#recipeResult").html(response);
          }
          else {
            $("#recipeResult").html("There were no recipes with the Category <span class='search-param'>" + categorypicked + "</span>. <br>Try searching again." );
          }         
          //scroll window to results
          $('html, body').animate({
            scrollTop: $(".results-col-xs").offset() -300
          }, 'slow');          
        },
        error: function (error) {
          $("#recipeResult").html("There was an error searching recipes. Please try again.");
        }
      });
    });


  // #endregion
  
  // #region GET CUISINE FROM SEARCH FILTER AND PASS TO FLASK

    $("#cuisine-select").change(function (event) {
      event.preventDefault();
      var cuisinepicked = $('#cuisine-select').find(":selected").text();
      var cuisine = cuisinepicked.trim();
      $.ajax({
        url: '/filter_by_cuisine/' + cuisine,
        contentType: 'application/json',
        data: JSON.stringify(cuisine),
        type: 'POST',
        success: function (response) {
          $("h3.section-subheading").html("Recipes searched by Cuisine: " + cuisinepicked);
          $('#cuisine-select').val("Select a Cuisine");
          if (response != "fail") {
            $("#recipeResult").html(response);
          }
          else {
            $("#recipeResult").html("There were no recipes with the Cuisine <span class='search-param'>" + cuisinepicked + "</span>. <br>Try searching again." );
          }         
          //scroll window to results
          $('html, body').animate({
            scrollTop: $(".results-col-xs").offset() -300
          }, 'slow');          
        },
        error: function (error) {
          $("#recipeResult").html("There was an error searching recipes. Please try again.");
        }
      });
    });

  // #endregion
  
  
  // #region GET ALLERGENS FROM SEARCH FILTER AND PASS TO FLASK

    $("#allergens-select").change(function (event) {
      event.preventDefault();
      var allergenspicked = $('#allergens-select').find(":selected").text();
      var allergens = allergenspicked.trim();
      $.ajax({
        url: '/filter_by_allergens/' + allergens,
        contentType: 'application/json',
        data: JSON.stringify(allergens),
        type: 'POST',
        success: function (response) {
          $("#searchResult").show();
          $("h3.section-subheading").html("Recipes searched by Allergens: " + allergenspicked);
          $('#allergens-select').val("Select Allergens");
          if (response != "fail") {
            $("#recipeResult").html(response);
          }
          else {
            $("#recipeResult").html("There were no recipes with the Allergens <span class='search-param'>" + allergenspicked + "</span>. <br>Try searching again." );
          }         
          //scroll window to results
          $('html, body').animate({
            scrollTop: $(".results-col-xs").offset() -300
          }, 'slow');          
        },
        error: function (error) {
          $("#recipeResult").html("There was an error searching recipes. Please try again.");
        }
      });
    });

  // #endregion  
  
  

  