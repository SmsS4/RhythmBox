base = "http://0.0.0.0:7000/"


var options = {
    autoClose: true,
    progressBar: true,
    enableSounds: true,
    sounds: {
        info: "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233294/info.mp3",
        // path to sound for successfull message:
        success: "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233524/success.mp3",
        // path to sound for warn message:
        warning: "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233563/warning.mp3",
        // path to sound for error message:
        error: "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233574/error.mp3",
    },
};

var toast = new Toasty(options);
toast.configure(options);
console.log("hey")


function logout() {
    localStorage.removeItem('token');
    window.location.href = base;
}

function checkToken(token){
    if (token == null) {
        console.log("token is null");
        return false
    }
    var valid = false;
    jQuery.ajax({
        url: 'validate_token'+'?token=' + token,
        success: function(valdiated) {
          valid = valdiated;
        },
        async:false
    });
    return valid
}

function init(token) {
    if (!checkToken(token)){
        $("#if_login").hide()
        $("#if_not_login").show()
        return
    }
    console.log(token);
    username = localStorage.getItem('username')
    $("#user").replaceWith('<a class="nav-link" href="/profile/' + username + '" id="user" >Profile</a>')
    $("#logout").show()
    $("#if_login").show()
    $("#if_not_login").hide()
}

function search() {
    console.log($("#search_input").val());
    window.location.href = base+"platform?string=" + $("#search_input").val();
}


function register() {
    username = $("#reg_username").val()
    password = $("#reg_password").val()
    email = $("#reg_email").val()
    name = $("#reg_name").val()
    console.log(username);
    console.log(password);
    console.log(email);
    console.log(name);
    $.post('register', {username:username, password:password, email:email, name:name},
        function(data){
            console.log(data);
            msg = data[0]
            status = data[1]
            console.log(status);
            console.log("Register")
            /// register successful
            if (status != "false"){
                console.log("good")
                toast.success(msg);
                $("#registerModal").modal('hide')
            }else {
                /// Register failed
              console.log("error");
                toast.error(msg);

            }


    }).fail(function(){
          console.log("error");
        toast.error("Unkown error. register failed");

    });
}


function login() {
    username = $("#username_field").val()
    password = $("#password_field").val()

    $.post('login', {username:username, password:password},
        function(token){
            console.log("Login")
            /// login succesfull
            if (token){
                localStorage.setItem('token', token);
                $("#loginModal").modal('hide')
                localStorage.setItem('username', username)
                toast.success("Login successfully");
                init(token);
            }else {
                /// login failed

              console.log("error");
              toast.error("Username or password is wrong");

            }

    }).fail(function(){
          console.log("error");
          toast.error("Unknown error. login failed");
    });

};


$(document).ready(function(){

    $('.header').height($(window).height());

    $("#logout").hide()

    $("#search_input").on('keypress',function(e) {
        if(e.which == 13) {
            search();
        }
    })

    //success toast




//    $('#successtoast').click(function() {
//
//    toast.success("This toast notification with sound");
//
//    });
//
//    $('#infotoast').click(function() {
//
//    toast.info("This toast notification with sound");
//
//    });
//
//    $('#warningtoast').click(function() {
//
//    toast.warning("This toast notification with sound");
//
//    });
//
//    $('#errortoast').click(function() {
//
//    toast.error("This toast notification with sound");
//
//    });


//    this is animation to scroll to section for nav bar buttons
  buttons = ["#homebutton", "#contactus", "#staffbutton", "#feautresbutton"]
  for(var i = 0; i < buttons.length; i++){
      $(buttons[i]).click(function(e) {
        e.preventDefault();
        $('html, body').animate({
          scrollTop: $($.attr(this, 'href')).offset().top
        }, 1000);
      });

    }
    init(localStorage.getItem("token"));
});


