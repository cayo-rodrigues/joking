` Handle the logic of commenting and seeing comments related to a joke `

function show_comment_box(joke_id)
{
    // Show a text area for users to comment in a given joke
    box_id = `#comment-box-${joke_id}`;
    // The comment box can be shown or hidden by clicking the same button again
    $(box_id).toggleClass('hidden_form');
}

function seeComments(joke_id)
{
    // Show all comments related to a given joke
    $(`#comments-at-${joke_id}`).toggleClass('hidden_form');

    comments = document.querySelector(`#comments-at-${joke_id}`);
    if (comments.innerHTML.trim() == "")
    {
        // it there is no comments on that joke yet, display a message to the user
        comments.innerHTML = `<span id="no_comments_at_${joke_id}">Hit &#128172; and be the first to share a comment! &#129299;</span>`;
    }

    // change text on button when comments are hidden, and change it back when they're not
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
    // handle logic for submiting a comment related to a given joke to the server
    nc_message = document.querySelector(`#no_comments_at_${joke_id}`);
    if (nc_message)
    {
        // if there are no comments related to that joke yet, hide the no comments message
        $(`#no_comments_at_${joke_id}`).addClass('hidden_form');
    }

    // get user's comment and make it a json before sending it to the server
    c = document.querySelector(`#comment-for-${joke_id}`).value;
    comment = {
        'comment': c
    }

    // send a post request to '/comment/<joke_id>', passing the comment as data to the server
    // when the server responds to the request, use the info received to execute a function
    $.post('/comment/' + joke_id, comment, function(info)
    {
        // hide the comment box where the user has typed his/her comment
        $(box_id).toggleClass('hidden_form');
        // show the comments related to that joke
        $(`#comments-at-${joke_id}`).removeClass('hidden_form');

        // display the newly added comment without needing to refresh the page
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