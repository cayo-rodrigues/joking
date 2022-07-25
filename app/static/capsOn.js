// wait fr a key press
document.addEventListener('keyup', (event) => {
    // if CapsLock is active
    if (event.getModifierState('CapsLock'))
    {
        // show an alert for the user saying that Caps lock is ons
        $('.caps_feedback').removeClass('hidden_form');
        $('.caps_feedback').html('Caps lock is on!');
    }
    else
    {
        // hide the alert
        $('.caps_feedback').addClass('hidden_form');
        $('.caps_feedback').html('');
    }
});