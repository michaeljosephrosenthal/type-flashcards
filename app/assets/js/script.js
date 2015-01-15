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
    $(selector).prev().removeClass("last");
    $(selector).addClass("success");
    flash("success");
    $('html body').animate({
        scrollTop: $(selector).offset().top
    }, 500);
    $(selector).next().find('input[name="read"]').focus();
}
/*
 * this part is confusing:
 * start with 2 retries ->  remove the 'three' and add the 'two' class -> 2 more retries, etc.
 */
retry_classes = ["", "two", "three"];
function correct_retry(selector, answer, retries){
    $(selector).addClass("warning");
    $(selector).find('input[name="read"]').val("");
    $(selector).find(".retries")
        .removeClass(retry_classes[retries])
        .addClass( retries > 0 ? retry_classes[--retries] : "")
        .attr('retries', retries);
    flash("warning");
}
function wrong(selector){
    $(selector).find('input[name="read"]').val("");
    $(selector).addClass("danger");
    flash("danger");
}
function handle_guess(selector){
    $form = $(selector);
    var input = $form.find('input[name="read"]').val();
    var answer = $form.find('input[name="answer"]').val();
    var retries = parseInt($form.attr('retries'));
    speak(answer);
    if(retries === 0 && input == answer){
        add_success_scroll($form);
    } else if (input == answer){
        correct_retry($form, answer, retries);
    } else {
        retries = retries > 0 ? retries : $form.attr('retries', 2);
        //console.log($(form.data('retries').val()));
        wrong($form, answer);
    }
}
$(document).ready(function(){
    $("form.read").submit(function(){
        event.preventDefault();
        handle_guess(this);
    });
});
