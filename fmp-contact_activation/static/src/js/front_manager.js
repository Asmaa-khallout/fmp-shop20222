$(document).ready(function () {
	/*
		Check if user is inactive then replace link to /my/activation
	*/
	$.ajax({
        url: '/check_user_activation',
        success: function(res){  
        	var json_value = JSON.parse(res)
            if (json_value["user_status"]=='inactive'){
				$('a').each(function() {
					if($(this).attr('href').indexOf('/contactus')>=0){
						$(this).attr('href', '/my/activation');
					}
				});
            }
        } 
    });
});

