var frameRate = 60;
var canvas;
var lastTime;

function init(fps) {
    canvas = document.getElementById('mycanvas');

    //Do nothing if canvas doesn't work
    if (canvas.getContext) {

        ctx = canvas.getContext('2d');
        frameRate = fps;

        //init game
        initGame();

        lastTime = new Date().getTime();

        timeInterval = 1000 / fps;
        setInterval(frameworkUpdate, timeInterval);

    }
    else {
        alert("Get a  modern browser with html5 support like firefox to play this game");
    }

}
function frameworkUpdate() {
    //Get elapsed time
    var currentTime = new Date().getTime();
    var dt = (currentTime - lastTime) / 1000.0;
    lastTime = currentTime;

    updateGame(dt);
    renderGame(dt);
}