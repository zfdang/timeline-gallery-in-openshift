$(document).ready(function() {
   // $.fn.editable.defaults.mode = 'inline'; // default = popup
   $('a.headline').editable();
   $('a.text').editable({mode:'inline', rows:4, });
   $('a.start_date').editable();
   $('a.visibility').editable({
     // value: 2,
     source: [
       { value: 'True', text: 'Public'}, 
       { value: 'False', text: 'Private'},
     ]
   });   // // $('.edit').editable('http://www.example.com/save.php');
   // // initialize all start_date
   // $("input.start_date").datepicker({
   //   dateFormat: "yy-mm-dd"
   // });

   // $("b.headline").editable("/admin/photos/update/headline", {
   //     indicator: "<img src='/static/image/indicator.gif'>",
   //     tooltip: "Click to edit headline...",
   //     event: "click",
   //     style: "inherit"
   //   });

   // $("b.text").editable("/admin/photos/update/text", {
   //     indicator: "<img src='/static/image/indicator.gif'>",
   //     tooltip: "Click to edit text...",
   //     event: "click",
   //     style: "inherit"
   //   });


   // // change behavior of bootstrap "close" button in alert-info 
   // $('.alert-info .close').click(function() {
   //   $(".alert-info").toggle(false);
   //   return false;
   // })

   // // submit start_date to server after new start_date is inputted
   // $("input.start_date").change(function() {
   //   photo_id = $(this).attr("photoid");
   //   start_date = this.value;

   //   $.ajax({
   //     type: "POST",
   //     // url: "{{ url_for("photos.update", target='start_date') }}",
   //     url: "/admin/photos/update/start_date",
   //     data: {
   //       "id": photo_id,
   //       "start_date": start_date,
   //     },
   //     dataType: 'json',
   //     success: function(msg) {
   //       // show alert message
   //       $("#alert-info-title").html(msg.status);
   //       $("#alert-info-message").html(msg.message);
   //       $(".alert-info").toggle(true);
   //     }
   //   });
   // });

 });
