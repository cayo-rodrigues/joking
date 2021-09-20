// wait until page is fully loaded
document.addEventListener('DOMContentLoaded', function() 
{
    // count clicks
    var click = 0;
    // select the dropdown icon and run a function when it's clicked
    $('#dropdown_button').click(function() 
    {
        click++;
        // when it's clicked twice, rotate it back
        if (click > 1)
        {
            $('#dropdown_icon').css({
                'transform': 'rotateX(0deg)',
                'transition': 'all 0.2s ease-in-out' 
            });
            // reset click count
            click = 0;
        }
        // in the first click, rotate icon
        else
        {
            $('#dropdown_icon').css({
                'transform': 'rotateX(180deg)',
                'transition': 'all 0.2s ease-in-out' 
            });
        }       
    });
});

/* this would achieve the same results: */

    // button.style.transform = 'rotateX(180deg)';
    // button.style.transition = 'all 0.2s ease-in-out';

/* but we'd have to run a: */
    // button = document.querySelector('#dropdown_button');
/* first of course */