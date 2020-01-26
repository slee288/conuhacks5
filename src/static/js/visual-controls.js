function toggle_pause(){
    if(document.getElementById("pause_button").src.includes("Pause.svg")){
        document.getElementById("pause_button").src = "images/Play.svg";
    }else{
        document.getElementById("pause_button").src = "images/Pause.svg";
    }
}

function update_time(){
    setInterval(function(){
        var today = new Date();

        var ap = "AM";
        var hour = today.getHours();
        var min = today.getMinutes();

        if(min < 10){
            min = "0" + min;
        }

        if(hour >= 12 && hour <= 23){
            ap = " PM";
            if(hour > 12) hour = hour % 12;
        }else{
            if(hour > 12) hour = hour - 12;
        }

        document.getElementById("time").innerHTML = hour + ":" + min + ap;
    })
}

