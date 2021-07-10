music_id = 0
music_name = ""
musics = []
premium = true

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

function play_music(music_id) {
    console.log(music_id);
    for (var j = 0; j < musics.length; j++){
        if(musics[j]["id"] == music_id){
            music_name = musics[j]["name"];
        }
    }
    $("#title").text(music_name);
    music_id = music_id;
    var audio = $("#player");
    $("#player").attr("src", "http://0.0.0.0:7000/music/"+music_id);
    audio[0].pause();
    audio[0].load(); //suspends and restores all audio element
//    audio[0].play();
    audio[0].oncanplaythrough = audio[0].play();
}

function downloadmusic() {
    if(premium){
        var link = document.createElement("a");
        // If you don't know the name or want to use
        // the webserver default set name = ''
        link.setAttribute('download', music_name);
        link.href = "http://0.0.0.0:7000/music/"+music_id;
        document.body.appendChild(link);
        link.click();
        link.remove();
    }else{
        toast.error("Free users can't download music");
    }
}

function search(){
    var string = $("#search-input").val();
    console.log(string);
    $.get('search', {string:string},
        function(data){
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
                $('#search-result-list').append('<li class="list-group-item clickable" onclick="play_music('+musics[i]["id"]+')">' + musics[i]["name"] + '</li>');
            }
            $('#search-result-list').append('<li class="list-group-item head-list">Artists</li>');
            for (var i = 0; i < artists.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable">' + artists[i]["name"] + '</li>');
            }
            $('#search-result-list').append('<li class="list-group-item head-list">Playlists</li>');
            for (var i = 0; i < playlists.length; i++){
                $('#search-result-list').append('<li class="list-group-item clickable">' + playlists[i]["name"] + '</li>');
            }




    }).fail(function(){
        console.log("error");
        toast.error("Unkown error");

    });
}


$(document).ready(function(){
    if($("#search-input").val()){
        search();
    }
});