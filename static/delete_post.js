function confirm_delete(id)
{
    joke_id = {
        'joke_id': id.split('_', 2)[1]
    }
    $('#r_u_shure_at_' + joke_id['joke_id']).toggleClass('hidden_form');
}

function delete_joke()
{
    $.post('/delete/joke', joke_id, function()
    {
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
    $('#r_u_shure_at_' + joke_id['joke_id']).toggleClass('hidden_form');
}

function uncomment(info)
{
    split = info.split('_', 3);
    comment_id = {
        'comment_id': split[1]
    }
    joke_id = split[2];

    $.post('/delete/comment', comment_id, function()
    {
        $('#comment_n_' + comment_id['comment_id']).remove();
        
        $(`#comments-at-${joke_id}`).toggleClass('hidden_form');
        seeComments(joke_id);
        $(`#c-dropdown-at-${joke_id}`).html('Hide comments');
    });
}