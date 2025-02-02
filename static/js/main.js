

$(document).ready(function(){
    const v1 = document.querySelector("#video1");
    const v2 = document.querySelector("#video2");
    const audio = document.querySelector("#bg-audio");
    audio.volume = 0.4

    v1.addEventListener("ended", ()=>{
        v1.setAttribute("hidden", true)
        v2.removeAttribute("hidden");
        $("#main-overlay").fadeIn();
    });


    $("#about-btn").on("click", e=>{
        $("#about").animate({
            left:"0"
        });

        $("#contact").animate({
            right:"-28rem"
        })
    });

    $("#about_close_btn").on("click", e=>{
        $("#about").animate({
            left:"-28rem"
        });
    });


    $("#contact-btn").on("click", e=>{
        $("#contact").animate({
            right:"0"
        });

        $("#about").animate({
            left:"-28rem"
        });
    });

    $("#contact-close-btn").on("click", e=>{
        $("#contact").animate({
            right:"-28rem"
        })
    });

    $("#register-btn").on("click", e=>{
        $("#form-overlay").toggleClass("hidden");
    });


    $("#unmute-btn").on("click", (e)=>{
        $("#unmute-btn").toggleClass("hidden")
        $("#mute-btn").toggleClass("hidden");
    
        audio.muted = false
        audio.play()
    });

    $("#mute-btn").on("click", (e)=>{
        $("#unmute-btn").toggleClass("hidden")
        $("#mute-btn").toggleClass("hidden");
        
        audio.pause()
    });
    
})

const closeOverlay = () =>{
    $("#form-overlay").toggleClass("hidden");
}


