/*Listerner sur la Page entière cf learn.jquery.com*/
$(document).ready(function (){
    function avancer(){
        $.post("/action",{direction: "avancer"});
        console.log("Avancer a marché");
    }
    function reculer(){
        $.post("/action",{direction: "reculer"});
        console.log("Reculer a marché");
    }
    function gauche(){
         $.post("/action",{direction: "gauche"});
        console.log("Gauche a marché");
    }
    function droite() {
        $.post("/action",{direction: "droite"});
        console.log("Droite a marché");
    }

    function stop() {
        $.post("/action",{direction: "stop"});
        console.log("Stop a marché");
    }

    function passage_auto() {
        $.post("/action",{direction: "passage_auto"});
        console.log("Le mode auto a marché");
    }

$('#b1').on("mousedown",avancer).on("mouseup",stop);
$('#b2').on("mousedown",reculer).on("mouseup",stop);
$('#b3').on("mousedown",gauche).on("mouseup",stop);
$('#b4').on("mousedown",droite).on("mouseup",stop);
$('#b5').on("mousedown",stop).on("mouseup",stop);
$('#b6').on("mousedown",passage_auto)




});









