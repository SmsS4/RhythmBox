
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
base = "http://0.0.0.0:8000/"


function logout() {
    localStorage.removeItem('token');
    window.location.href = base;
}

function init(token) {
    if (token == null) {
        console.log("token is null");
        return
    }
    console.log(token);
    username = localStorage.getItem('username')
    $("#user").replaceWith('<a class="nav-link" href="/profile/' + username + '" id="user" >Profile</a>')
    $("#logout").show()
}



function register() {
    username = $("#reg_username").val()
    password = $("#reg_password").val()
    phone = $("#reg_phone").val()
    name = $("#reg_name").val()
    console.log(username);
    console.log(password);
    console.log(phone);
    console.log(name);
    $.post('register', {username:username, password:password, phone:phone, name:name},
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
  buttons = ["#homebutton", "#contactus", "#staffbutton"]
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

