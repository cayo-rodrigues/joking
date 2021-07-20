document.addEventListener('keyup', (event) => {
    if (event.getModifierState('CapsLock'))
    {
        $('.caps_feedback').removeClass('hidden_form');
        $('.caps_feedback').html('Caps lock is on!');
    }
    else
    {
        $('.caps_feedback').addClass('hidden_form');
        $('.caps_feedback').html('');
    }
});