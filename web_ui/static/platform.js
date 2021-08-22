music_id = 0
music_name = ""
current_playlist_id = 0
playlist_musics = []
musics = []
premium = (localStorage.getItem('account_type') == "2")
tof = false

function gohome() {
    window.location.href =  window.location.href.split("/platform")[0];
}
function showprofile(username){
    window.location.href =  window.location.href.split("/platform")[0]+"/profile/" + username;
}
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

function set_add_remove_pl(){
    base = $("#addtopld").attr('src').split("addmpl.png")[0];
    base = base.split("removempl.png")[0]
    for (var i = 0; i < playlist_musics.length; i++){
        if(playlist_musics[i]["uid"] == music_id){
            $("#addtopld").attr('src', base + "removempl.png")


            document.getElementById('addtopld').onclick = remove_music_from_pl;
            return;
        }
    }



    // not found in playlist
    $("#addtopld").attr('src', base + "addmpl.png")
    document.getElementById('addtopld').onclick = addmusictopl;

}

function play_music(music_id_to_play) {
    console.log(music_id_to_play);
    for (var j = 0; j < musics.length; j++){
        if(musics[j]["id"] == music_id_to_play || musics[j]["uid"] == music_id_to_play){
            music_name = musics[j]["name"];
        }
    }
    $("#title").text(music_name);
    music_id = music_id_to_play;
    var audio = $("#player");
    $("#player").attr("src", "music/"+music_id_to_play); /// changed
    audio[0].pause();
    audio[0].load(); //suspends and restores all audio element
//    audio[0].play();
    audio[0].oncanplaythrough = audio[0].play();
    set_add_remove_pl();
}

function downloadmusic() {
    if(premium){
        var link = document.createElement("a");
        // If you don't know the name or want to use
        // the webserver default set name = ''
        link.setAttribute('download', music_name);
        link.href = "music/"+music_id; /// changed
        document.body.appendChild(link);
        link.click();
        link.remove();
    }else{
        toast.error("Free users can't download music");
    }
}

function search(){
    var string = $("#search-input").val();
    var token = localStorage.getItem('token');
    console.log(string);
    $.get('search', {token:token, string:string},
        function(data){
            if ('Shared Playlist' in data){

                $("#search-result-list").empty()
                $('#search-result-list').append('<li class="list-group-item head-list">Shared Playlist</li>');
                plist = data['Shared Playlist']
                for (var i = 0; i < plist.length; i++){
                    $('#search-result-list').append('<li class="list-group-item clickable" onclick="showpl('+plist[i]["id"]+')">' + plist[i]["name"] + '</li>');
                }
                return;
            }
            console.log(data);
            var artists = data['artists']
            musics = data['musics']
            var playlists = data['playlists']
            console.log(artists);
            console.log(musics);
            console.log(playlists);
            $("#search-result-list").empty()


            $('#search-result-list').append('<li class="list-group-item head-list">Musics</li>');

            for (var i = 0; i < musics.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable" onclick="play_music('+musics[i]["id"]+')">' + '<span class="qual">' +  musics[i]["quality"] + '</span>   ' + '<span class="qual">' +  musics[i]["genera"] + '</span>   '+ musics[i]["name"] + '</li>');
            }
            $('#search-result-list').append('<li class="list-group-item head-list">Artists</li>');
            for (var i = 0; i < artists.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable" onclick="showprofile('+ "'" + artists[i]["id"]+"'" +')" >' + artists[i]["name"] + '</li>');
            }
            $('#search-result-list').append('<li class="list-group-item head-list">Playlists</li>');
            for (var i = 0; i < playlists.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable" onclick="showpl('+playlists[i]["id"]+')">' + playlists[i]["name"] + '</li>');
            }




    }).fail(function(){
        console.log("error");
        toast.error("Unkown error");

    });
}

function share(playlist_id){

 var username = prompt("Please enter new manager username");
     $.post('share', {playlist_id:playlist_id, username:username},
        function(data){
            if(!data){
                    toast.success("Shared");

                    }else{
                    toast.error(data);
                    }


    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}
function shared_with_me(){
    var token = localStorage.getItem('token');

    $.get('swm', {token:token},
        function(data){
            console.log(data);
            var playlists = data
            $("#search-result-list").empty()

            $('#search-result-list').append('<li class="list-group-item head-list">Shared With Me</li>');
            for (var i = 0; i < playlists.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable" onclick="showpl('+playlists[i]["id"]+')">' + playlists[i]["name"] + '</li>');
            }


    }).fail(function(){
        console.log("error");
        toast.error("Unkown error");

    });
}


$(document).ready(function(){
    if($("#search-input").val()){
        search();
        $("#current_playlist").empty()
        getmypl();

//        $('#current_playlist').append('<li class="list-group-item head-list">Musics</li>');
    }
});

function remove(playlist_id){
    tof = true;
    $.post('delpl', {token:localStorage.getItem('token'), playlist_id:playlist_id},
        function(data){
            if(data == null){
                toast.success("Playlist removed");
                getmypl();
            }else{
                toast.error(data);
            }
    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}

function getmypl(){

    $("#my_playlists").empty()
        $.get('get_my_pl', {username:localStorage.getItem('username')},
        function(data){



            $("#my_playlists").empty()
             for (var i = 0; i < data.length; i++){
                if (data[i]["name"] != "Followings" && data[i]["name"] != "Discover"){
                    $('#my_playlists').append(
                        '<li class="list-group-item clickable" onclick="showpl('+data[i]["id"]+')">' +  '<span class="qual" onclick="addmanager('+data[i]["id"]+')">' +  "Add manager" + '</span>   ' +  '<span class="qual" onclick="remove('+ data[i]["id"] +')">' +  "Remove" + '</span>   ' +  '<span class="qual" onclick="share('+ data[i]["id"] +')">' +  "Share" + '</span>   '+ data[i]["name"] +'</li>'
                    );
                }else{
                    $('#my_playlists').append(
                        '<li class="list-group-item clickable" onclick="showpl('+data[i]["id"]+')">' + data[i]["name"] +'</li>'
                    );
                }
            }

            $('#my_playlists').append(
                    '<li class="list-group-item clickable" style="opacity:0.5" onclick="addnew_playlist()">' +  "Add New PlayList" + '</li>'
                );


    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}

function addnew_playlist(){
    var name = prompt("Please enter your playlist name");
     $.post('addpl', {token:localStorage.getItem('token'), name:name},
        function(data){

                    toast.success("Playlist created");
            getmypl();

    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}
function youarefree(){
  toast.error("Free users can't listen to 320 musics");
}

function showpl(playlist_id) {
    if (tof){
        tof = false;
        return;
    }
    $.get('getpl', {uid:playlist_id},
        function(data){
            current_playlist_id = playlist_id;
                musics = data['musics']
                $("#title2").text(data['name']);
                $("#plink").text(window.location.href.split("/platform")[0]+"/platform?string=sharedpl$"+data['name']);
                playlist_musics = musics;
        $("#current_playlist").empty()
         for (var i = 0; i < data['musics'].length; i++){
                if(!premium && data['musics'][i]["quality"] == 320){
                    $('#current_playlist').append(
                        '<li class="list-group-item clickable" onclick="youarefree()">' + '<span class="qual">' +  data['musics'][i]["quality"] + '</span>   ' + data['musics'][i]["name"] + '</li>'
                    );
                }else{
                    $('#current_playlist').append(
                        '<li class="list-group-item clickable" onclick="play_music('+data['musics'][i]["uid"]+')">' + '<span class="qual">' +  data['musics'][i]["quality"] + '</span>   ' + data['musics'][i]["name"] + '</li>'
                    );
                }
            }
    set_add_remove_pl();


    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
    console.log(playlist_id);
}

function addmusictopl() {


    $.post('add_music_pl', {token: localStorage.getItem('token'), playlist_uid: current_playlist_id, music_uid: music_id},
        function(data){

                if(data){
                    toast.error(data);
                }else{
                    toast.success("Added to playlist");
                    showpl(current_playlist_id);

                }
            }



    ).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}


function remove_music_from_pl(){
 $.post('remove_music_pl', {token: localStorage.getItem('token'), playlist_uid: current_playlist_id, music_uid: music_id},
        function(data){
                set_add_remove_pl();
                if(data){
                    toast.error(data);
                }else{
                    toast.success("Added to playlist");
                    showpl(current_playlist_id);

                }
            }



    ).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}

function addmanager(playlist_id){

 var username = prompt("Please enter new manager username");
     $.post('add_owener_pl', {token:localStorage.getItem('token'),uid:playlist_id, username:username},
        function(data){
            if(!data){
                    toast.success("Manager Added");

                    }else{
                    toast.error(data);
                    }


    }).fail(function(){
        console.log("error");
        toast.error("Unknown error");

    });
}