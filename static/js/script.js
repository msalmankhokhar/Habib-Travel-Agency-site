let slides = document.querySelectorAll('.slide');

let no_of_slides = slides.length

let slide_No_as_arg = 1;
let counter_as_arg = 1;
let mode_forward = true;

slides.forEach((slide, index) => {
    slide.style.left = `${index * 100}%`;
    console.log("done")
});

function slideNext(slideNow) {
    slides.forEach(slide => {
        // let value = counter*(80);
        slide.style.transform = `translateX(-${slideNow * 100}%)`;
        // counter = counter + 1
    });
}
function slidePrev(slideNow) {
    slides.forEach(slide => {
        // let value = counter*(80);
        slide.style.transform = `translateX(${(slideNow - 1) * (-100)}%)`;
        // counter = counter + 1
    });
}

document.body.onload = function playSlides() {
    setInterval(() => {
        if (slide_No_as_arg < no_of_slides && mode_forward == true){
            slideNext(slide_No_as_arg);
            console.log(slide_No_as_arg);
            slide_No_as_arg++;
            if (slide_No_as_arg == no_of_slides){
                mode_forward = false;
            }
        }       
        else if (mode_forward == false){
            slide_No_as_arg--;
            slideNext(slide_No_as_arg);
            console.log(slide_No_as_arg);
            if (slide_No_as_arg == 0){
                mode_forward = true;
            }
        }       
    }, 3000);
}