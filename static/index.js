$(document).ready(function() {

  if (SHOULD_SHOW_TABLE) $( ".data" ).show();
  else $( ".data" ).hide();
 
  data = $.parseJSON(RETURNED_DATA);
  if (data.length > 0) {
    for (var i=0; i<data.length; i++) {
      var title = data[i].title;
      var url = data[i].url;
      var startDateTime = data[i].start_time;
      var category = data[i].category;
      var minPrice = data[i].min_price;
      var maxPrice = data[i].max_price;
      var zipCode = data[i].zip_code;
      var venue = data[i].venue;
      
      var row = `<tr><td>${i}</td>
                     <td>${title}</td>
                     <td><a href="${url}">Link</a></td>
                     <td>${startDateTime}</td>
                     <td>${category}</td>
                     <td>${minPrice}</td>
                     <td>${maxPrice}</td>
                     <td>${zipCode}</td>
                     <td>${venue}</td>
                 </tr>`;
      $( ".data tbody" ).append(row);
    } 
  }

  var input = $("#userIn").val;
  $( "#userIn" ).focusin(function() {
    $( this ).attr("placeholder", "");
  });
  
  $( "#userIn" ).focusout(function() {
    $( this ).attr("placeholder", "what are you looking for?");
  });
  
  $('#userIn').keypress(function (e) {
    if (e.which == 13) {
      if (form[0].value != "" || form[0].value != " ") {
        form.submit();
        return false;
      }
    }
  });

});
