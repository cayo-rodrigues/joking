// when document is ready, that is, when page is fully loaded
$(document).ready(() => {
    // listen for clicks on any rating button
    $('.rate').click((event) => {
        // which joke is this?
        joke_id = event.target.id;
        // is the user voting or unvoting?
        vote = event.target.name;

        // send ajax post request to server and get the joke's updated rating back
        $.post(`/rate/${joke_id},${vote}`, (rating) => {
            // visually update joke's rating count
            document.querySelector(`#rating_for_${joke_id}`).innerHTML = rating;
            
            // display icon to let user know he has already voted for that joke
            if (vote == 'add') {
                $(`#voted_for_${joke_id}`).removeClass();
                $(`#voted_for_${joke_id}`).addClass('add');
            }
            // or hide icon when he unvotes
            else {
                $(`#voted_for_${joke_id}`).removeClass();
                $(`#voted_for_${joke_id}`).addClass('remove');
            }
        });
    });
});