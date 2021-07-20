function show_comment_box(joke_id)
{
    box_id = `#comment-box-${joke_id}`;
    $(box_id).toggleClass('hidden_form');
}

function seeComments(joke_id)
{
    $(`#comments-at-${joke_id}`).toggleClass('hidden_form');

    comments = document.querySelector(`#comments-at-${joke_id}`);
    if (comments.innerHTML.trim() == "")
    {
        comments.innerHTML = `<span id="no_comments_at_${joke_id}">Hit &#128172; and be the first to share a comment! &#129299;</span>`;
    }

    button = document.querySelector(`#c-dropdown-at-${joke_id}`);
    if (button.innerHTML == 'Hide comments')
    {
        button.innerHTML = 'Show comments';
    }
    else
    {
        button.innerHTML = 'Hide comments';
    }
}

function post_comment(joke_id)
{
    nc_message = document.querySelector(`#no_comments_at_${joke_id}`);
    if (nc_message)
    {
        $(`#no_comments_at_${joke_id}`).addClass('hidden_form');
    }

    c = document.querySelector(`#comment-for-${joke_id}`).value;
    //console.log(comment);
    comment = {
        'comment': c
    }

    $.post('/comment/' + joke_id, comment, function(info)
    {
        $(box_id).toggleClass('hidden_form');
        $(`#comments-at-${joke_id}`).removeClass('hidden_form');

        c_box = document.querySelector(`#comments-at-${joke_id}`);
        c_box.innerHTML+=`<div class="comment" id="comment_n_${info['comment_id']}">` +
                            '<p>' +
                                `<a href="/profile/${info['username']}"><img class="comment_pic" src="${info['ppic']}"></a>` +
                                '<b>' + info['username'] + '</b>' +
                                `<span class="delete_post" type="button" id="uncomment_${info['comment_id']}_${joke_id}" onclick="uncomment(this.id)">&#10006;</span>` +
                            '</p>' +
                            '<p>' +
                                '<pre class="container">' + comment['comment'] + '</pre>' +
                            '</p>' +
                        '</div>';

        $(`#no_comments_at_${joke_id}`).remove();
    });
}