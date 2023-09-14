/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

function toSendMessage(email){

  let confrm= confirm("Are you sure you want to send Email?");

  if(!confrm)
    return
     // Endpoint URL
  const endpointUrl = '/clubSendMail'; // Change this to the correct endpoint URL

  // Data to be sent in the POST request
  const data = {
    email: email
  };

  // Send the POST request to the Flask endpoint using jQuery AJAX
  $.ajax({
    type: 'POST',
    url: endpointUrl,
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (response) {
      // Handle the response here if needed
      console.log('Response from Flask endpoint:', response);
    },
    error: function (error) {
      console.error('Error:', error);
    }
  });

}
