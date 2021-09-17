$(document).ready(() => {

    ignore = [
        'Enter', 'Tab', 'CapsLock', 'Shift', 'Control', 'Alt', 
        'Meta', 'Escape', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 
        'ArrowDown', 'NumLock', 'End', 'PageDown', 'PageUp', 
        'Home', 'Insert', 'PrintScreen', 'ScrollLock', 'Pause', 
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 
        'F10', 'F11', 'F12'
    ];

    document.querySelectorAll('.auto-feedback').forEach(function(f)
    {
        f.addEventListener('keyup', (event) => {            
            if (!ignore.includes(event.key))
            {
                inputs = {};
                inputs[f.name] = f.value;
                // send to server both password and confirmation together
                // to avoid 400 bad request
                if (f.name == 'confirmation')
                {
                    inputs['password'] = document.querySelector('#input_password').value;
                }
                else if (f.name == 'password')
                {
                    inputs['confirmation'] = document.querySelector('#input_confirmation').value;
                }
                give_feedback(inputs);
            }
        });
    });
});

function avoid_refresh(step)
{
    $('#registration_form').submit((event) => {
        event.preventDefault();
        if (step == 'registration')
        {
            give_feedback();
        }
    });
}

function give_feedback(inputs)
{
    inputs = inputs || 0;

    if (inputs == 0)
    {
        fields = document.getElementsByClassName('form-control');
        inputs = {};
        for (let i = 0; i < fields.length; i++)
        {
            inputs[fields[i].name] = fields[i].value;
        }
    }

    $.post('/register', inputs, (feedback) => {

        if (feedback == '200 OK')
        {
            //send_email(inputs['email']);
            return window.location.replace("/login");
        }
        
        for (let i in feedback)
        {
            $(`#${i}`).html(feedback[i]);
                        
            if (feedback[i] != '&#129303; Perfect &#129303;')
            {
                $(`#${i}`).css({
                    'color': 'rgb(92,0,0)'
                });
                $(`#input_${i}`).css({
                    'border-color': 'crimson',
                    'box-shadow': '0px 0px 3px crimson'                    
                });
            }
            else
            {
                $(`#${i}`).css({
                    'color': 'rgb(0,92,0)'
                });
                $(`#input_${i}`).css({
                    'border-color': 'green',
                    'box-shadow': '0px 0px 3px green'                    
                });
            }
        }
    });
}
/*
function send_email(email)
{
    $.post('/email', email, () => {
        console.log("Please enter the verification code we've sent to your email");
    });
}
*/