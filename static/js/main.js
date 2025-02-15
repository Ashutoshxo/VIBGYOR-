const audioElement = document.getElementById('audioElement');
const playButton = document.getElementById('playButton');

playButton.addEventListener('click', function() {
    if (audioElement.paused) {
        audioElement.play();
        playButton.textContent = '⏸'; // Change to pause icon
    } else {
        audioElement.pause();
        playButton.textContent = '▶'; // Change to play icon
    }
});

<button class="play-button" id="playButton">▶</button>
