music = document.querySelector(".music");

music.volume = 0.5;

function toggle_music() {
    if (music.paused) {
        music.play();
    }
    else {
        music.pause();
    }
}