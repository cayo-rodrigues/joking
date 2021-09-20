` Handle joke deletion `

function confirm_delete(id)
{
    // when user attempts to delete one of his jokes, show him a message of confirmation
    joke_id = {
        'joke_id': id.split('_', 2)[1]
    }
    $('#r_u_shure_at_' + joke_id['joke_id']).toggleClass('hidden_form');
}

function delete_joke()
{
    // if user click 'yes', then ask the server to delete that joke from the database
    $.post('/delete/joke', joke_id, function()
    {
        // visually erase the joke and its comments without having to reload the page
        $('#hr_at_' + joke_id['joke_id']).css({
            'display': 'none'
        });
        $('#comments-at-' + joke_id['joke_id']).html('');
        $('#comments-at-' + joke_id['joke_id']).css({
            'display': 'none'
        });
        $('#joke_n_' + joke_id['joke_id']).html('');
    });
}

function quit_delete()
{
    // if user clicks 'no' or the 'x' button again, the deletion confirmation message desapears
    $('#r_u_shure_at_' + joke_id['joke_id']).toggleClass('hidden_form');
}


/* Handle comment deletion */
function uncomment(info)
{
    // get info regarding which comment at what joke the user wants to delete
    split = info.split('_', 3);
    comment_id = {
        'comment_id': split[1]
    }
    joke_id = split[2];

    // send that info to the server
    $.post('/delete/comment', comment_id, function()
    {
        // when the server finishes deleting the comment, visualy erase the comment, without having to refresh the page
        $('#comment_n_' + comment_id['comment_id']).remove();
        
        // 'reload' the comments section of that joke, so that the 'no comments message' can appear, if that's the case
        $(`#comments-at-${joke_id}`).toggleClass('hidden_form');
        seeComments(joke_id);
        $(`#c-dropdown-at-${joke_id}`).html('Hide comments');
    });
}