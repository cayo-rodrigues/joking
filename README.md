# PHUN

#### Video Demo:  https://youtu.be/ZWTFRmjrFxE

#### Description:

## General

Designed using _Flask_ framework, **Phun** is a social network for sharing puns, or jokes.

You can see other's jokes, share your own, like and comment. There is a page for the newly added ones, and the best rated puns. Something I think that would be nice, is a search engine to look for phunners(other users), or maybe a feature to keep track of how many likes each user has in total, and create a page to display the best phunners. Whoever would be the first, would become the Jo**king**. It'd be cool too if there was a *"forgot my password"* feature and maybe a way for users to change credentials. But implementing all of these would demand too much time and effort, more than needed and expected for the Final Project, and even more than I can currently give. 

I began to build this web application shortly after concluding **CS50x**. It took me a couple months to finish it. Every time I wanted to implement a new feature I would search the net and learn a lot in the process. I really enjoyed the experience. But then, after miserably failing to deploy the app to _Heroku_ and a lot of headache, I decided to take **CS50w** so that I could eventually learn how to put something to work on the internet for real.

But still I wanted to properly finish the course, so I decided to ask the _Discord_ community if it was allowed to submit a final project like mine that runs only locally. They said it was no problem, and indeed, there are many web applications like that in the _Gallery of Final Projects_. That cheered me up to finally record a video and submit my final project.

However, looking through the project, I realized that the design would be way much better if using _Django_, since the application deals a lot with user data, and also for organization sake. But by the time I made this project, I didn't know _Django_. And as I was reading each piece of code, along with the comments, it made me feel some of the thrill I felt back then, when I was learning new things and getting excited seeing things working as expected. So I decided to stay with _Flask_ and just made some slight changes to the code, improving the design, and fixing a few bugs that showed up. Regarding the templates, I bet I could do better, there must be better ways for implementing some of those features, but things were already working well. And despite a little confusion at first (second and maybe third) glance, it really seemed to make sense, considering the amount of knowledge I had back then.

There is one thing that I kind of copy pasted from the **CS50** staff, which is the fancy responsive navbar made with bootstrap classes. Of course I made some changes, but the credits go for them. Besides that, I grabbed the _login_required_ function from them too.

Now let's head into the details of this project, exploring each of it's files.



## app.py

This file contains only view functions, to deal with many GET and POST requests at all urls.

- ### index: 

    The _index_ view function, associated with the default route(`'/'`) redirects the user to his/her profile page. But if the user is not logged in, then he/she is redirected to the login page.

- ### profile:

    By visiting `/profile/<username>` this function is called to display a user's profile page. It handles POST requests for them to share new jokes (unless their visiting another user's profile page). It interacts with the *SQLite* database and *Flask sessions* to get user data and pass it to the *DOM*. In this page you can see your jokes, sort them by date or rating, choose your profile picture, delete your jokes, vote for them and even delete your account. 

    Regarding the profile pictures, they're not stored in the SQL db. Why? Well, I didn't know that was possible when developing this application, and I took a totally different path. The pictures are stored in an images folder inside the static folder.

    It requires the user to be logged in. This logic is implemented via a decorator, using the _login_required_ function, designed by the **CS50** staff on _Problem Set 9_.
    
- ### sort:

    Receives a GET request (`/sort/<order>`) containing the desired order to sort the jokes in a profile page, and store this order (either `"date_time"` or `"rating"`) in session. This function returns None.

    Why isn't inside the profile function? Well, this seemed as a more practical approach, since the profile function already does many things and deals with both GET and POST requests. Instead of adding more condition checking inside the profile route, I decide to add another route.

    Login is required.

- ### upload_pic:

    The URL route associated with this function (`/upload_pic`), accepts only POST requests. It handles the picture uploading feature logic. If the input received exists and is valid, then the former profile picture is deleted and the new one is saved.

    Login is required.

- ### rate:

    Handles joke voting at `/rate/<vote>` where `vote` may be either `"add"` or `"remove"`.

    If the user wants to vote for (aka like, rate or pun up) a joke, or to remove his vote, the rate function interacts with the *SQLite* database in order to do so. It returns the updated rating of that joke to the JS callback function as JSON, so that the rating can be visually incremented when user puns up a joke.

    Login is required.

- ### posts:

    Display all posts. A post is nothing but a joke, along with the profile picture and username of its author and it's possible comments and rating. This function interacts with the database to retrieve information from all users.
    
    By visiting `/posts/<sort_order>` this view works for two different pages in the website. Users can visit the *newest* (ordered by date) or the *phuniest* (ordered by rating) posts page.
    
    Login is required.
    
- ### comment:

    Add a comment to a given joke with id of `joke_id`. The `/comment/<joke_id>` route only accepts POST requests. It interacts with the *SQL* database to add the comment that the user has (hopefully!) entered as Markdown in a `textarea`.

    One interesting thing that I learned when writing this view is the `cursor.lastrowid` (where `cursor = connection.cursor()` and `connection = sqlite3.connect('phun.db')`) property. The primary key of a row in a *SQL* db table is autoincremented when adding new rows. And in this case, I had to pass the comment id to the JS callback function (This route is requested through an Ajax request). So the `.lastrowid` property allowed me to generate HTML using the JS file to display the newly added comment, and let the `/delete/<stuff>` route (more on that in a bit) clearly identify it.

    Besides that, the *user id*, the *username* and the user *profile picture path* are also passed to the JS callback function to display the full comment block.

    Login is required.

- ### delete_post:

    The _delete_post_ function is associated with the `/delete/<stuff>` route. This route accepts only POST requests.

    Users can delete their own jokes, comments and even their accounts. When they're deleted, all content related to them are also deleted. 

    So for example, let's say that there is a user with the username of `youser`. If `youser` decides to delete his whole account, his profile picture, all of his jokes, comments and votes (both the ones received and the ones he gave) disappear. Supposing that another user had a joke with a rating of 10, for which `youser` had previously voted for, then now the rating would fall to 9.

    Login is required.

- ### login:

    When receiving a GET request, display a form to the user. When receiving a POST request, validate user input and log him/her in if everything is fine. Otherwise, provide feedback through *Flask flashed messages*.

- ### register:

    Display a form for the user to type in his username, password, password confirmation and email address. A JS script sends info to this function via *Ajax POST requests*. With this info, we can identify which field user is currently filling, so that we can give instant feedback (handled by another function, inside _helpers.py_ file).

    If any user input is not valid, the registration process won't be procced. Although instant feedback is given though POST requests, even if all inputs are valid, the registration will only be finished when user clicks the register button.

    After signing up, user is redirected to the login page and notified through a *Flask flashed message* that the registration was successful.

- ### logout:

    Logs user out, by clearing the session. User is redirected to login page and notified that he/she is logged out.



## helpers.py

This file has some helper functions, called by the views in _app.py_ to perform some tasks.

- ### login_required:

    Designed by the CS50 staff, this function, when applied via _decorators_ (@) to routes, redirects users to the login page when they're not logged in, that is, when their user id has not yet been added to the session.

- ### find_pic:

    Look for users profile pictures and return their path.

- ### allowed_file:

    Ensure the uploaded picture is of an allowed type. The allowed types are `.gif`, `.jpg`, `.jpeg` and `.png`.

    If it's allowed, return `True`, else return `False`.

- ### check_key:

    Check if a given dictionary has a certain key. Returns `True` or `False`.

- ### erase_picture:

    Accepts as argument the path for a picture and deletes the picture if it's not the default profile picture.

- ### list_to_html:

    Converts a list of tupples from markdown to html. 

    That's useful because when fetching multiple results from a *SQL query* you get a list of tupples, that means, each individual element of the list is a tupple. That's strange, because each tupple has only one element. Why not just return a simple list, or maybe a tupple entirely? Well, that's how the `sqlite3` library works. But this is minimal in comparison to its simplicity for querying databases.

    This function is used to convert jokes and comments from Markdown (I mean, they're only _interpreted_ as markdown, they're not stored in *actual* Markdown files, just as *text* in the database) to HTML.

    Returns a converted list, not as a list of tupples, but as a list of lists. 😵🤪

- ### give_feedback:

    Ensure correct input and give corresponding feedback to user when filling the registration form.

    This is by far the most exciting feature I've implemented. It feels really good to see that instant feedback popping up as I type.

    The `give_feedback` function is called by the `register` view, which itself is called by an Ajax POST request coming from `feedback.js`. It receives three arguments:

    - *The value of the input fields* user is submitting, such as username, password, email, or even all fields at once (as by clicking the register button);
    - *Flags* to identify which fields are being submitted; 
    - *And a bool* to indicate if user is submitting the whole form or not.
    
    It returns a dictionary containing all feedbacks, positive or not.



## .env

It contains my *Gmail* username, used by `give_feedback` function to check email validity using the `validate_email` function from the `validate_email` library.



## phun.db

A SQLite database to store users data. It has four tables. They are:

- comments
- jokes
- votes
- users

I did my best at designing it, trying to avoid redundancies, but surely one could do better. The `c_username` column which stands for `"commenter's username"` seems like a redundancy (and in essence, it is), but it avoids additional queries. The famous "Memory x Speed" tradeoff comes into scene, and I chose to gain speed in trade for some memory. One thing that influenced my choice too was the complexity. I'm not so good at *SQL* when it comes to nesting queries, so I decided to do that to avoid wasting unnecessary hours with something that could be solved by just allocating a little more memory.



## requirements.txt

Contains everything that I've pip installed to develop this application. There may be more things than needed, but if so, that's because I did not develop this project in a virtual environment. Didn't know much about it or why I should use it back then 🤪.



## Templates

Taking advantage of _Jinja2_, Flask's templating language, I was able to avoid much redandancy, at the cost of some complexity.

- ### layout.html:

    Home of the `<head>` tag, containing all the meta information, _Bootstrap_ and _JQuery_ stuff, as well as a link to a `styles.css` file and one to a JS script for animating the dropdown icon in the navigation bar.

    The navbar only appears when user is logged in. It was basically a copy-paste from the distribution code of **CS50**'s Problem Set 9, Finance. Of course I customized it, but still I would have had a lot of extra work finding out how to build something like this from scratch, or studying Bootstrap classes, so the credits go all for the staff.

    This HTML page has a `<main>` tag whose content changes for each page visited, but all other contents of the layout are extended to the other pages (except for the `<title>`, of course, that one changes too).

- ### login.html:

    Displays a form for the user to type in their username or email and password in order to log in, which sends info to the `/login` url. There is a link to `/register` route. In the login page, a message is displayed to the user when Caps Lock is on, thanks to the `capsOn.js` file.

- ### register.html:

    Display a form, in order to get user's desired username, password and e-mail. The form interacts with the `register` view function and with `feedback.js`. Also in this page user is notified when Caps Lock is on.

- ### profile.html:

    A sheet-like page with all user info. Thanks to _Jinja2_ templating language this file is used both when visiting your own profile page and when visiting other's pages.

    Here you'll see a profile picture, on which you can click to upload a new picture and a form that users can use to post new jokes. Also, scrolling down you'll see all your posts and you can interact with them. If you want to sort your posts, you can do so using a select menu. And at the bottom right of the page you'll see a little options menu displaying what e-mail you used when creating your account and a "delete my account" option which pops up a confirmation message before deleting it.
    
- ### posts.html:

    Show all posts ever made from all users. The sort order varies according to which page user is visiting, whether it is _Newest_ or _Phuniest_.

    In these pages user can vote for jokes (or remove his votes), comment (or remove his comments), and delete his own posts.

- ### flashed_message.html:

    Instead of having _Flask flashed messages_ in _layout.html_, I decided to keep it as a separated file and include it in other pages using Jinja's _include_ syntax. It allows for a wider variety of how and where to display and style the message.




## Static

The static folder contains all JavaScript files and a CSS stylesheet, as well as a folder for storing images.

- ### styles.css:

    Home of all style information. Bigger than expected (and maybe more than needed), it has 416 lines. Nothing fancy though. And I must admit that writing CSS can sometimes be very cool, but also very tricky. Sometimes a certain style simply won't apply and you gotta search the net to figure out why. Or maybe sometimes an _overflow-x_ pops up out of nothing and you have to work around it. But I really enjoyed the experience and learned a lot.

- ### capsOn.js:

    When any key is pressed, check if Caps Lock is on. If so, select an element in the DOM and modify its CSS and HTML in order to display a message to the user, else, hide the message.

- ### comment.js:

    Handles the logic of commenting and seeing comments related to a joke. The `show_comment_box` function receives a `joke_id` as argument and display a `textarea` for user to type in their comment and a button for them to submit it.

    The `seeComments` function is called by the click of a button, to display all comments related to a joke. It also changes the inner HTML of the button to indicate what the next click on it will do.

    And lastly, the `post_comment` function gets user input from the `textarea` and send it to the server via an *Ajax POST request*. Then a callback function uses the info received from the server to immediately display the newly added comment.

- ### delete_post.js:

    Handle joke and comment deletion.

    When user attempts to delete one of his jokes, a confirmation message pops up. If user clicks 'yes' then an *Ajax request* is sent to the server, for it to delete the joke. When the server finishes the job, then a *callback function* visually deletes the post. But if user clicks 'no' or the 'x' button then the confirmation message disappears.

    Also there is the `uncomment` function, which receives as input both the comment id and the joke id and sends an *Ajax POST request* to the server, for it to delete the comment. Then, the comment is deleted from the document, without having to reload the page.

- ### dropdown_click.js:

    Handles the logic for animating the navbar dropdown menu icon. It is only shown in mobile devices.

- ### feedback.js:

    Give dynamic feedback to users when they're filling the registration form.

    First, we wait until the document is ready (page is fully loaded) and then *declare and array* with all the names of keys that *should be ignored* when giving feedback. These key names are the same key names from `event.key` , not from `event.code`.

    Then we select all HTML elements with the `.auto-feedback` class and run a function for each one of them. This function (which is applied to all the elements selected) adds an event listener to wait for key releases (decided to use `"keyup"` instead of `"keydown"` to avoid multiple calls if user holds a key down) that checks if the key pressed is among the ones to be ignored (defined in the `ignore` array). If they're not to be ignored, declare a JSON object that will store user input. Then, get the `name` property of the input field and its `value` (that is, what the user has typed so far). If user is inputting password or confirmation fields, then both are added to the JSON.

    After that, the `give_feedback` function is called and the user info gathered so far is passed as argument.

    The `avoid_refresh` function is called when user submits the whole form, and it simply prevents the page from refreshing and then calls the `give_feedback` function.

    The `give_feedback` function may be called in two ways: via form submission or key input. So the `inputs` argument in this function is optional. If the whole form is being submitted, then all user input is sent to the server. Otherwise, send only the value of the field in which user is currently typing. After getting a response from the server, if the user has been successfully registered, redirect him/her to the login page. It is only going to happen when the register button is clicked. Otherwise, instant feedback messages will show up right at the bottom of the field in which user is typing. Negative feedback messages are red and positive are green.

- ### my_profile.js:

    Deals with somethings that users are able to do in their own profile pages.

    When profile picture is clicked, simulate a click to an input of type file in a hidden form. This allows users to choose a new profile picture by simply clicking on it. When some file is selected, then another click is simulated to submit the form and upload the new picture.

    Also there's the `r_u_shure` function, which is called when users attempt to delete their accounts. It pops up a big confirmation message at the center of the screen.

- ### rate.js:

    Handle the logic of voting for a joke or removing a vote from a joke.

    When any rating button is clicked, figured out what joke is being rated and what action is the user performing, whether he's adding or removing his vote. We get this information via the _id_ and the _name_ of the clicked button.

    An *Ajax POST request* is sent to the server, and the server returns the updated rating of that joke. We then instantly update the rating count and display an icon to let users know which joke they've voted for, or hide icon when they remove their vote.

- ### sort_jokes.js:

    Called when user uses the select menu at any profile page to sort the jokes by rating or by newest. Sends an *Ajax POST request* to `/sort/<order>`, the server then stores the desired order in session and the callback *refreshes only the jokes section* of the page. 

    Using session works because the `/profile/<username>` route when accessed via a GET request checks the session to see if user has changed the default jokes display order, and uses this information to define in which order the jokes should be queried and passed to the DOM.

    

    - ## Images:

        The _static_ folder also contains an _images_ folder in which are stored all icons, profile pictures and all other images used the application.



## Final thoughts:

That's it. 🤓

🙆‍♂️🙆‍♂️🙆‍♂️🙆‍♂️ (The pasta dance)

☝️🙂☝️ (Ronaldinho's samba)
