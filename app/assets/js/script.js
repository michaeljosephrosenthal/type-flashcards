var kanya = {};
function speak(text){
    var msg = new SpeechSynthesisUtterance(text);
    msg.voice = kanya;
    speechSynthesis.speak(msg);
}

window.speechSynthesis.onvoiceschanged = function() {
    kanya = speechSynthesis.getVoices().filter(
                function(voice) { return voice.name == 'Kanya'; })[0];
};
var flash_time = 300;
function flash(fclass){
    clearTimeout();
    $("html").addClass(fclass);
    setTimeout(function () {
        $("html").removeClass(fclass);
    }, flash_time);
}
