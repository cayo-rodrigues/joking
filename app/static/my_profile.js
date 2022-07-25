document.addEventListener('DOMContentLoaded', () => {
    `That's how we bind clicks on one element to another`

    // when profile picture is clicked
    $('.profile_pic').click(() => {
        // simulate a click to choose a file
        document.querySelector('#ppic_choose').click();
    });
    // when some file is selected
    $('#ppic_choose').change(() => {
        // simulate a click to submit the form and upload the picture
        document.querySelector('#ppic_upload').click();
    });
});

/* Show a confirmation message when users attempt to delete their account */
function r_u_shure()
{
    $('.pop_up_center').toggleClass('hidden_form');
    $('.pop_up_center').html(
        `
        <div class="confirm_account_delete">
            <h2>Are you shure?</h2>
            <p>
                <form action="/delete/account" method="POST">
                    <button class="btn-danger" type="submit">Yes</button>
                    <input type="button" class="btn-primary" onclick="r_u_shure()" value="No"></input><br>
                    <span style="color:orange">&#9888;</span>
                    <span style="font-size: 1.1rem"><b>This cannot be undone!</b></span>
                    <span style="color:orange">&#9888;</span>
                </form>
            </p>
        </div>
        `
    )
}