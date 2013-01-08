// init datapicker
$('#start_date').datepicker();

// set click function for submit button in form
$("form#setting").submit(function validation() {
            if($("form #headline").val() == "") {
                alert("Headline can't be empty");
                return false;
            }
            if($("form input#start_date").val() == "") {
                alert("Start Date can't be empty");
                return false;
            }
    });
