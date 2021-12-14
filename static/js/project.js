'use strict';



// AJAX CALL FOR RSVP 
function addguestRSVP(evt) {
  evt.preventDefault();

const url = '/rsvp_update.json';
const formData = {rsvp_attend: $('#rsvp_attend').val(), event_id: $('#event_id').val()};

$.get(url, formData, response => {
  $('#rsvp-div').html(`${response.rsvp_status}`).hide();
})
}
$('#rsvp-form').on('submit', addguestRSVP);

/////////////////////////////////////////////////////////////////////////////
// PROFILE PICTURE CLOUDINARY

// Once HTML file is loaded
$(document).ready(function(){

    // Grabs the user's profile picture
    $.post('/get-profile-pic', response => {
  
      // Setting response to a variable
      let profile_pic = response
  
      // If the user's profile picture exists
      if (profile_pic != "False") {
        
        // Display user's profile picture on page
        $('#profile-pic-display').append('<img src="' + profile_pic + '" class="profile_photo"/>');
      
      // If user's profile picture doesn't exist
      } else {
  
        // Display default profile picture on page
        $('#profile-pic-display').append('<img src="/static/img/default1.jpg" class="profile_photo"/>');
      }
    });
  });


  /////////////////////////////////////////////////////////////////////////////
// PROFILE PICTURE CLOUDINARY SMALL VERSION

// Once HTML file is loaded
$(document).ready(function(){

    // Grabs the user's profile picture
    $.post('/get-profile-pic', response => {
  
      // Setting response to a variable
      let profile_pic = response
        
      // If the user's profile picture exists
      if (profile_pic != "False") {
        
        // Display user's profile picture on page
        $('#profile-pic-display2').append(`<img src="${profile_pic}" class="update-photo-size"/>`);
      
      // If user's profile picture doesn't exist
      } else {
  
        // Display default profile picture on page
        $('#profile-pic-display2').append('<img src="/static/img/default1.jpg" class="update-photo-size"/>');
      }
    });
  });

/////////////////////////////////////////////////////////////////////////////
// EVENT PICTURE CLOUDINARY

// Once HTML file is loaded
$(document).ready(function(){
const event_id = $("#event_id").val();
    // Grabs the user's profile picture
    $.post(`/get-event-pic/${event_id}`, response => {
    
      // Setting response to a variable
      let event_pic = response
  
      // If the user's profile picture exists
      if (event_pic != "False") {
        
        // Display user's profile picture on page
        $('#event-pic-display').append('<img src="' + event_pic + '" class="event_photo"/>');
      
      // If user's profile picture doesn't exist
      } else {
  
        // Display default profile picture on page
        $('#event-pic-display').append('<img src="/static/img/default2.jpg" class="event_photo"/>');
      }
    });
  });

/////////////////////////////////////////////////////////////////////////////
function createGuestlist(evt) {
  evt.preventDefault();
  
  const url = '/create_guest_list.json';
  const formData = {fname: $('#fname').val(), lname: $('#lname').val(), event_id: $('#event_id').val()};
  
  $.get(url, formData, response => {
    console.log(response);
    $('#list').append(`<p>${response.first_name} ${response.last_name}: <b>${response.rsvp_status}</b></p>`);
  })
  
 }
 $('#new-guest-form').on('submit', createGuestlist);
 

/////////////////////////////////////////////////////////////////////////////

// AJAX CALL FOR CREATING GUEST COMMENT POST
function createGuestcomment(evt) {
  evt.preventDefault();

const url = '/create_guest_comment.json'
const formData = {guest_comment: $('#guest_comment').val(), event_id: $('#event_id').val()};

$.get(url, formData, response => {
  // console.log(response);
  // need to append a paragraph that contains the text of the post versus using .html
  $('#guest-comment-div').append (`<b><p style="text-align: center" class="response">Your post was submitted! Please refresh the page to view your posting: ${response.guest_post}</p></b>`);
})
}
$('#guest-comment-form').on('submit', createGuestcomment);

/////////////////////////////////////////////////////////////////////////////

// AJAX CALL FOR CREATING HOST COMMENT POST

function createHostcomment(evt) {
  evt.preventDefault();

const url = '/create_host_comment.json'
const formData = {host_comment: $('#host_comment').val(), event_id: $('#event_id').val()};

$.get(url, formData, response => {
  
  $('#host-comment-div').append (`<b><p style="text-align: center" class="response">Your post was submitted! Please refresh the page to view your posting: ${response.host_post}</p></b>`);
})
}
$('#host-comment-form').on('submit', createHostcomment);

/////////////////////////////////////////////////////////////////////////////
// PLAN EVENT FORM //





            






/////////////////////////////////////////////////////////////////////////////

// (function () {
//     const second = 1000,
//           minute = second * 60,
//           hour = minute * 60,
//           day = hour * 24;
  
//     //I'm adding this section so I don't have to keep updating this pen every year :-)
//     //remove this if you don't need it
//     let today = new Date(),
//         dd = String(today.getDate()).padStart(2, "0"),
//         mm = String(today.getMonth() + 1).padStart(2, "0"),
//         yyyy = today.getFullYear(),
//         nextYear = yyyy + 1,
//         dayMonth = "09/30/",
//         birthday = dayMonth + yyyy;
    
//     today = mm + "/" + dd + "/" + yyyy;
//     if (today > birthday) {
//       birthday = dayMonth + nextYear;
//     }
//     //end
    
//     const countDown = new Date(birthday).getTime(),
//         x = setInterval(function() {    
  
//           const now = new Date().getTime(),
//                 distance = countDown - now;
  
//           document.getElementById("days").innerText = Math.floor(distance / (day)),
//             document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
//             document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
//             document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);
  
//           //do something later when date is reached
//           if (distance < 0) {
//             document.getElementById("headline").innerText = "COUNTDOWN ENDED!";
//             document.getElementById("countdown").style.display = "none";
//             document.getElementById("content").style.display = "block";
//             clearInterval(x);
//           }
//           //seconds
//         }, 0)
//     }());









