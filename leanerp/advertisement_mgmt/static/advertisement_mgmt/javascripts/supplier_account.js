// Submit post on submit
$('#supplier_monthly_account').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

$('#supplier_account_period').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    update_supplier();
});

// AJAX for posting
function create_post() {
    $.ajax({
        url : "/query_supplier_account/", // the endpoint
        type : "POST", // http method
        data : $('#supplier_monthly_account').serialize(), // data sent with the post request
        // handle a successful response
        success : function(json) {
            $('#supplier_monthly_account').val(''); // remove the value from the input
            $("#pay").empty();
            $("#pay").append('<thead><tr><th>月份</th><th>起算日</th><th>結算日</th><th>結算應付金額</th><th>動作</th></tr></thead>');
            var num_of_jsondata = json.length;
            if(num_of_jsondata == 0){
            	$("#pay").append('<tbody><tr><td>查無資料</td><td></td></tbody>');
            }else{
                $("#pay").append('<tbody>');
	            for (var i = num_of_jsondata-1; i >= 0; i--) {
	            	//$("#pay").prepend("<li>Month: " + json[i]["month"] + ", Pay: " + json[i]["pay"] + "</li>");
                    $("#pay").append('<tr><td>' + json[i]["month"] + '</td><td>' + 
                                     json[i]["start"] + '</td><td>' +
                                     json[i]["end"] + '</td><td>' +
                                     json[i]["pay"] + '</td><td>' + 
                                     '<button target="_blank" supplier="' + 
                                     json[i]["code"] + '" month="' + json[i]["month"] + 
                                     '" class="checkbtn btn btn-info pull-right">' + 
                                     ' 查看 </button></td></tr>');
	            }
                $("#pay").append('</tbody>');
            }
            //$("#pay").text("month: " + json.pay.0);
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function update_supplier() {
    $.ajax({
        url : "/supplier_account_period/", // the endpoint
        type : "POST", // http method
        data : $('#supplier_account_period').serialize(), // data sent with the post request
        // handle a successful response
        success : function(json) {
            $('#supplier_account_period')[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}