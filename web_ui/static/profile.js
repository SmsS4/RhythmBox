
$(document).ready(function(){
    $("#name").val(localStorage.getItem('name'));
    $("#description").val(localStorage.getItem('description'));
    if (localStorage.getItem('publisher') == "true") $("#req_pub_div").hide()
    if (localStorage.getItem('account_type') == "2") $("#req_pre_div").hide()
    $('.header').height($(window).height());
    token = localStorage.getItem('token');
    ok = false;
    publisher = false;
    if (token){
         jQuery.ajax({
            url: 'get_account'+'?token=' + token,
            success: function(account) {
                if(account){
                    console.log(account);
                    ok = (account['username'] == $("#usern").text().trim());
                    publisher = account['publisher']
                  }
            },
            async:false
        });
    }
    if (!ok) publisher = false;
    if (publisher) {
            $(".publisher_menu").css("visibility", "visible")

    }else{
            $(".publisher_menu").css("visibility", "hidden")

    }
    if (ok){
        $(".hidden_if_not_user").css("visibility", "visible")
//        $("#upload_profile").show()
//        $("#upld_btn").show()
//        $("#upld_btn2").show()
    }else{
        $(".hidden_if_not_user").css("visibility", "hidden")

//        $("#upload_profile").hide()
//        $("#upld_btn").hide()
//        $("#upld_btn2").hide()
    }

});

function upld() {
    if(ok){
        $("#brws").click()
    }
}

$(document).on("click", ".browse", function() {
  var file = $(this)
    .parent()
    .parent()
    .parent()
    .find(".file");
  file.trigger("click");
});
$('input[type="file"]').change(function(e) {
  var fileName = e.target.files[0].name;
  $("#file").val(fileName);

  var reader = new FileReader();
  reader.onload = function(e) {
    // get loaded data and render thumbnail.
    document.getElementById("preview").src = e.target.result;
  };
  // read the image file as a data URL.
  reader.readAsDataURL(this.files[0]);
});


$(document).ready(function(e) {
  $("#image-form").on("submit", function() {
    token = localStorage.getItem('token');
    $("#msg").html('<div class="alert alert-info"><i class="fa fa-spin fa-spinner"></i> Please wait...!</div>');
    $.ajax({
      type: "POST",
      url: "change_photo?token="+token,
      data: new FormData(this), // Data sent to server, a set of key/value pairs (i.e. form fields and values)
      contentType: false, // The content type used when sending data to the server.
      cache: false, // To unable request pages to be cached
      processData: false, // To send DOMDocument or non processed data file it is set to false
      success: function(data) {
        if (data == 1 || parseInt(data) == 1) {
          location.reload();
          $("#msg").html(
            '<div class="alert alert-success"><i class="fa fa-thumbs-up"></i> Data updated successfully.</div>'
          );
        } else {
          $("#msg").html(
            '<div class="alert alert-info"><i class="fa fa-exclamation-triangle"></i> Extension not good only try with <strong>GIF, JPG, PNG, JPEG</strong>.</div>'
          );
        }
      },
      error: function(data) {
        $("#msg").html(
          '<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> There is some thing wrong.</div>'
        );
      }
    });

  });


  $("#music-form").on("submit", function() {
    token = localStorage.getItem('token');
    $("#msg").html('<div class="alert alert-info"><i class="fa fa-spin fa-spinner"></i> Please wait...!</div>');
    $.ajax({
      type: "POST",
      url: "upload_music?token="+token+"&name="+$("#music_name").val()+"&genera="+$("#genera").val(),
      data: new FormData(this), // Data sent to server, a set of key/value pairs (i.e. form fields and values)
      contentType: false, // The content type used when sending data to the server.
      cache: false, // To unable request pages to be cached
      processData: false, // To send DOMDocument or non processed data file it is set to false
      success: function(data) {
        if (data == 1 || parseInt(data) == 1) {
          $("#msg").html(
            '<div class="alert alert-success">Data updated successfully.</div>'
          );
        } else {
          $("#msg").html(
            '<div class="alert alert-info"><i class="fa fa-exclamation-triangle"></i> Extension not good only try with <strong>GIF, JPG, PNG, JPEG</strong>.</div>'
          );
        }
      },
      error: function(data) {
        $("#msg").html(
          '<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> There is some thing wrong.</div>'
        );
      }
    });
  });
});

function edit(){
    name = $("#name").val()
    description = $("#description").val()
    localStorage.setItem('name', name);
    localStorage.setItem('description', description);
    req_publisher = String($("#req_pub").is(':checked'))
    req_premium = String($("#req_pre").is(':checked'))
    $.post(
        '/edit',
        {
            token:token,
            name:name,
            description:description,
            req_publisher:req_publisher,
            req_premium:req_premium
        },
        function(data){},
    ).fail(
        function(){}
    );
    location.reload();
}
