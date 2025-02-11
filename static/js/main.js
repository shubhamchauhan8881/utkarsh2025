

// $(document).ready(function(){
//     const v1 = document.querySelector("#video1");
//     const v2 = document.querySelector("#video2");
//     const audio = document.querySelector("#bg-audio");
//     audio.volume = 0.4

//     v1.addEventListener("ended", ()=>{
//         v1.setAttribute("hidden", true)
//         v2.removeAttribute("hidden");
//         $("#main-overlay").fadeIn();
//     });


//     $("#about-btn").on("click", e=>{
//         $("#about").animate({
//             left:"0"
//         });

//         $("#contact").animate({
//             right:"-28rem"
//         })
//     });

//     $("#about_close_btn").on("click", e=>{
//         $("#about").animate({
//             left:"-28rem"
//         });
//     });


//     $("#contact-btn").on("click", e=>{
//         $("#contact").animate({
//             right:"0"
//         });

//         $("#about").animate({
//             left:"-28rem"
//         });
//     });

//     $("#contact-close-btn").on("click", e=>{
//         $("#contact").animate({
//             right:"-28rem"
//         })
//     });

//     $("#register-btn").on("click", e=>{
//         $("#form-overlay").toggleClass("hidden");
//     });


//     $("#unmute-btn").on("click", (e)=>{
//         $("#unmute-btn").toggleClass("hidden")
//         $("#mute-btn").toggleClass("hidden");
    
//         audio.muted = false
//         audio.play()
//     });

//     $("#mute-btn").on("click", (e)=>{
//         $("#unmute-btn").toggleClass("hidden")
//         $("#mute-btn").toggleClass("hidden");
        
//         audio.pause()
//     });
    
// })

// const closeOverlay = () =>{
//     $("#form-overlay").toggleClass("hidden");
// }



function startCountdown(targetDate) {
    function updateTimer() {
        const now = new Date().getTime();
        const timeLeft = targetDate - now;

        if (timeLeft <= 0) {
            clearInterval(interval);
            return;
        }

        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        $("#cd-days").text(days);
        $("#cd-hours").text(hours);
        $("#cd-minutes").text(minutes);
        $("#cd-seconds").text(seconds);
    }
    updateTimer();
    const interval = setInterval(updateTimer, 1000);
}


const hideEventPopUp = (e) => {
        $("#eventPopup").animate({ top: "200%" });
        setTimeout(() => {
            $("#popup-card").addClass("hidden");
            $("#popup-skeleton-loader").removeClass("hidden");
        }, 300)
    }


const ShowEventPopUp = (eventname) => {
    $("#eventPopup").animate({ top: "0" });
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: `/events/details/${eventname}`,
        method: "GET",
        headers: { 'X-CSRFToken': csrftoken },

        success: (data, status, xhr) => {
            $("#popup-skeleton-error").addClass("hidden");
            $("#popup-skeleton-loader").addClass("hidden");

            $("#event-name").text(data.title);
            
            $("#accordion-1").html(data.general_rules);
            $("#accordion-2").html(data.event_rules);

            $("#event-details").html(data.details);

            $("#event-date").text(data.event_date);
            $("#event-venue").text(data.venue);

            $("#popup-image-1").attr("src", data.image);
            $("#popup-image-2").attr("src", data.image2);
            $("#popup-image-3").attr("src", data.image3);
            $("#popup-image-4").attr("src", data.image4);

            if(data.is_enrolled){
                $("#event-enroll").addClass("hidden");
                $("#event-unenroll")
                .removeClass("hidden")
                .on("click", e=>{
                    window.location.href = `/events/${eventname}/unenroll/${data.is_enrolled}`;
                });
            }else{

                 $("#event-unenroll").addClass("hidden");
                $("#event-enroll").removeClass("hidden");
                $("#event-enroll").on("click", (e)=>{
                    window.location.href = `/events/enroll/${eventname}`;
                })
            }

            $("#popup-card").removeClass("hidden");

        },
        error: (xhr, str) => {
            $("#popup-skeleton-loader").addClass("hidden");
            $("#popup-card").addClass("hidden");
            $("#popup-skeleton-error").removeClass("hidden");
        },
    })
}


function navigate(e){
    window.location.href = e;
}


function hideSideNav(){
    $("#sideNav").toggleClass("w-0");
}



function toggleRnG(){
    $("#rng").toggleClass("hidden")
}

function toggleAccordion(id) {
    $(`#accordion-${id}`).toggleClass("hidden");
    $(`#arrow-down-${id}`).toggleClass("hidden");
    $(`#arrow-up-${id}`).toggleClass("hidden");

}