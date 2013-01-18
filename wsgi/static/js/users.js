$(document).ready(function() {
   // $.fn.editable.defaults.mode = 'inline'; // default = popup
   $('a.username').editable();
   $('a.email').editable();
   $('a.password').editable();
   $("i.user-delete").click(function() {
     photo_id = $(this).attr("id");

     $.ajax({
       type: "POST",
       url: user_update_url,
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