// function toggle_pause(){
//     if(document.getElementById("pause_button").src.includes("Pause.svg")){
//         // document.getElementById("pause_button").src = "images/Play.svg";
//         document.getElementById("pause_button").src = "{{url_for('static', filename='images/Play.svg')}}";
//     }else{
//         document.getElementById("pause_button").src = "images/Pause.svg";
//     }
// }
//
function update(){
    //Updating time from frontend
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

        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(postPosition);
        }else{
            console.log("Geolocation is not available in this browser");
        }

        function postPosition(position){
            $.ajax({
                type:"POST",
                url:"/loc",
                data:{
                    "latitude":position.coords.latitude,
                    "longitude":position.coords.longitude,
                    "curr_time": hour
                }
            })
        }
    }, 10000)

    setInterval(function(){
        // if(navigator.geolocation){
        //     navigator.geolocation.getCurrentPosition(postPosition);
        // }else{
        //     console.log("Geolocation is not available in this browser");
        // }
        //
        // function postPosition(position){
        //     $.ajax({
        //         type:"POST",
        //         url:"/loc",
        //         data:{
        //             "latitude":position.coords.latitude,
        //             "longitude":position.coords.longitude
        //         }
        //     })
        // }

    }, 10000)
}
