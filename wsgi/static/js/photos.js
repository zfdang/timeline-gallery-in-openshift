$(document).ready(function() {
   // $.fn.editable.defaults.mode = 'inline'; // default = popup
   $('a.headline').editable();
   $('a.text').editable({
      mode: 'inline',
      rows: 4,
   });   
   $('a.start_date').editable();
   $('a.visibility').editable({
     // value: 2,
     source: [
       { value: 'True', text: 'Public'}, 
       { value: 'False', text: 'Private'},
     ]
   });
   $("i.photo-delete").click(function() {
     photo_id = $(this).attr("id");

     $.ajax({
       type: "POST",
       url: photo_update_url,
       data: {
         "pk": photo_id,
         "name": 'delete',
         "value":''
       },
       dataType: 'json',
       success: function(msg) {
         // show alert message
         $("#alert-info-title").html(msg.status);
         $("#alert-info-message").html(msg.message);
         $(".alert-info").toggle(true);

         // remove photo in the list
         if(msg.status == "success")
            $("tr#" + photo_id).remove();
       }
     });

   });

});