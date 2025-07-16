let index = 1;
showSlides(index);



function showSlides(n) {
    const images = document.getElementsByClassName("images");
    if (n > images.length) {
        index = 1;
    }
    else if (n < 1) {
        index = images.length;
    }
    for (let i = 0; i < images.length; ++i) {
        images[i].style.display = "none";
    }
    images[index - 1].style.display = "block";
    const larrow = document.querySelector(".prev");
    const rarrow = document.querySelector(".next");
    
    if (images.length > 1) {
        larrow.style.display = "block";
        rarrow.style.display = "block";
    }
}

function nextSlide(n) {
    index += n
    showSlides(index)
}
