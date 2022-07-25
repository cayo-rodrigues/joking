` Give dynamic feedback to users when they're filling the registration form `

$(document).ready(() => {

    // key pressess to be ignored when giving feedback
    ignore = [
        'Enter', 'Tab', 'CapsLock', 'Shift', 'Control', 'Alt', 
        'Meta', 'Escape', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 
        'ArrowDown', 'NumLock', 'End', 'PageDown', 'PageUp', 
        'Home', 'Insert', 'PrintScreen', 'ScrollLock', 'Pause', 
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 
        'F10', 'F11', 'F12'
    ];

    // select all html elements with the 'auto-feedback' class and run a function for each one of them
    document.querySelectorAll('.auto-feedback').forEach(function(f)
    {
        // 'f' corresponds to each input 'field'
        f.addEventListener('keyup', (event) => {
            // when user presses a key that is not to be ignored into some of the input fields
            if (!ignore.includes(event.key))
            {
                inputs = {};
                // 'f.name' identifies which field the user is filling, and 'f.value' is what is in it so far
                inputs[f.name] = f.value;
                // send to server both password and confirmation together to avoid 400 bad request
                if (f.name == 'confirmation')
                {
                    inputs['password'] = document.querySelector('#input_password').value;
                }
                else if (f.name == 'password')
                {
                    inputs['confirmation'] = document.querySelector('#input_confirmation').value;
                }
                // let another function do the actual feedback using the info we gathered
                give_feedback(inputs);
            }
        });
    });
});

/* Prevents page from refreshing when form is submitted */
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

/* this function may be called in two ways: via form submission or key input,
    so the 'inputs' argument is optional. */
function give_feedback(inputs)
{
    inputs = inputs || 0;
    // if form is being submitted, then get all the user input from all fields
    if (inputs == 0)
    {
        fields = document.getElementsByClassName('form-control');
        inputs = {};
        for (let i = 0; i < fields.length; i++)
        {
            inputs[fields[i].name] = fields[i].value;
        }
    }
    // send ajax post request to server, passing in the user inputs as data
    $.post('/register', inputs, (feedback) => {
        if (feedback == '200 OK')
        {
            // if the user has been succesfully registred, redirect him/her to the login page
            return window.location.replace("/login");
        }
        
        // loop through all feedback messages received from the server
        for (let i in feedback)
        {
            // display each message below in its corresponding input field
            $(`#${i}`).html(feedback[i]);
            
            // style messages and input fields according to the feedback
            if (feedback[i] != '&#129303; Perfect &#129303;')
            {
                // red for negative
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
                // green for positive
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