function validateForm() {
  var username = document.forms["myForm"]["username"].value;
  var email = document.forms["myForm"]["email"].value;
  var password = document.forms["myForm"]["password"].value;
  var reg = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
  

  if (username == "") {
    document.getElementById('errormsg').innerHTML="Username cannot be empty";
    return false;
  }
  else if(username.length<5)
  {
    document.getElementById('errormsg').innerHTML="Username must be more than 5 char";
    return false;
  }
  else if (email == "") {
    document.getElementById('errormsg').innerHTML="Email cannot be empty";
    return false;
  }

  else if (reg.test(email) == false) 
  {
    document.getElementById('errormsg').innerHTML="Email is invalid";
      return false;
  }
  else
  return true;
}



function sowModelwithImage(imageUrl, songUrl, descUrl, hidden_watch_later_val, songtitle, download_song) {
  $('#exampleModalCenter').modal('show')
  $("#image-show").attr('src', `/media/${imageUrl}`)
  $("#play-music").attr('src', `/media/${songUrl}`)
  $("#desc").html(`${descUrl}`)
  $("#hidden_val").val(`${hidden_watch_later_val}`)
  $(".song-title").html(`${songtitle}`)
  $("#download-song").attr('href', `/media/${download_song}`)
  }



  $('.btn-close').click(function () {
    $('#play-music').trigger("pause");
  });


  $(document).ready(function(){
  $("#listen_later").click(function(){
    $("h6").show();
    });
  });


  $( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    $( "#tags" ).autocomplete({
      source: 'autosuggest',
      
    });
    
  } ); 



  
