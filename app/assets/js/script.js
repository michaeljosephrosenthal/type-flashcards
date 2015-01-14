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
function add_success_scroll(selector){
    flash("success");
    $(selector).addClass("success");
    $('html body').animate({
        scrollTop: $(selector).offset().top
    }, 500);
    $(selector).next().find('input[name="read"]').focus();
}
function correct_retry(selector, answer){
    $(selector).addClass("warning");
    $(selector).find('input[name="read"]').val("");
    $(selector).find(".retries .btn-danger:visible").first().hide();
    flash("warning");
}
function wrong(selector){
    $(selector).find('input[name="read"]').val("");
    $(selector).addClass("danger");
    flash("danger");
}
var retries = 0;
$(document).ready(function(){
    $("form.read").submit(function(){
        $form = $(this); event.preventDefault();
        input = $form.find('input[name="read"]').val();
        answer = $form.find('input[name="answer"]').val();
        speak(answer);
        if(retries > 0 && input == answer){
            retries -= 1;
            correct_retry($form, answer);
        } else if (input == answer){
            add_success_scroll($form);
        } else {
            retries = retries > 0 ? retries : 2;
            wrong($form, answer);
        }
    });
});
