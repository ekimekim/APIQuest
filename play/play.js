var character = "Monty";

var viewElapsed = 0;
var viewPending;
var viewTimeout = 1;

var tileCount = [30, 15]; //[30, 15];
var canvasSize = [992, 465];

var entities = [];
var sprites = {};

function initGame() {
    console.log("Loading start 0.8d");

    sprites["player"] = loadImage("images/entityPlayer.png");
    sprites["orc"] = loadImage("images/entityOrc.png");
    sprites["skelly"] = loadImage("images/entitySkelly.png");
    sprites["bard"] = loadImage("images/entityBard.png");

    view();

}
function loadImage(name) {
    var image = new Image();
    image.src = name;
    return image;
}
function updateGame(dt) {
    //Request game state
    //Preform lerping
    viewElapsed += dt;
    //console.log("Update " + String(elapsed));

    if (!viewPending
    && viewElapsed >= viewTimeout) {
        view();
    }
}

function renderGame(dt) {
    var tileSize = [32, 32];//[canvasSize[0] / tileCount[0], canvasSize[1] / tileCount[1]];

    ctx.fillStyle = "#FFFFAA";
    ctx.fillRect(0, 0, canvasSize[0], canvasSize[1]);

    //Render objects
    for (i = 0; i < entities.length; ++i) {
        if (entities[i].name == character) {
            ctx.fillStyle = "#0000FF";
        }
        else {
            ctx.fillStyle = "#FF0000";

        }
        ctx.fillRect(entities[i].pos[0] * tileSize[0], entities[i].pos[1] * tileSize[1], tileSize[0], tileSize[1]);

        //Entities are a twice as tall as the tiles they stand in
        ctx.drawImage(sprites[entities[i].entityType], entities[i].pos[0] * tileSize[0], (entities[i].pos[1] - 1) * tileSize[1], tileSize[0], tileSize[1] * 2);
        //console.log("Draw " + entities[i].name + " at " + entities[i].pos);
    }
}

function view() {
    viewPending = true;
    $.get("http://http://localhost:56189/View.ashx?character=" + character, viewRecieved);
    console.log("view");
}

function viewRecieved(data) {
    viewElapsed = 0;
    viewPending = false;
    console.log("view recieved: " + data);

    statesRecieved = eval('(' + data + ')');

    entitiesToRemove = [];
    statesUsed = [];

    //Apply all the new states
    for (i = 0; i < entities.length; ++i) 
    {
        entityVisible = false;
        for (j = 0; j < statesRecieved.length; ++j) 
        {
            if (entities[i].name == statesRecieved[j].name) {
                entityVisible = true;
                statesUsed.push(j);

                applyEntityChanges(entities[i], statesRecieved[j]);

                break;
            }
        }
        if (!entityVisible)
            entitiesToRemove.push(i);
    }

    //Remove all the non visible entities
    for (i = entitiesToRemove.length - 1; i >= 0; --i) {
        console.log(entities[entitiesToRemove[i]].name + " no longer visible");
        entities = entities.slice(entitiesToRemove[i], 1);
    }

    //Remove all the used states  
    for (i = statesUsed.length - 1; i >= 0; --i) {
        statesRecieved = statesRecieved.slice(statesUsed[i], 1);
    }

    //Add all the new states
    for (i = 0; i < statesRecieved.length; ++i) {
        console.log(statesRecieved[i].name + " is now visible");
        entities.push(statesRecieved[i]);
    }
}

function applyEntityChanges(entity, newState) {
    if (entity.pos != newState.pos) {
        console.log(entity.name + " moved to " + String(newState.pos));
        entity.pos = newState.pos;
    }
}
