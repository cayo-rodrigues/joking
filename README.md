# PHUN

#### Video Demo:  <URL HERE>

#### Description:

## General

Designed using _Flask_ framework, **Phun** is a social network for sharing puns, or jokes.

You can see other's jokes, share your own, like and comment. There is a page for the newly added ones, and the best rated puns. Something I think that would be nice, is a search engine to look for phunners(other users), or maybe a feature to keep track of how many likes each user has in total, and create a page to display the best phunners. Whoever would be the first, would become the Jo**king**. It'd be cool too if there was a *"forgot my password"* feature. But implementing all of these would demand too much time and effort, more than needed and expected for the Final Project, and even more than I can currently give. 

I began to build this web application shortly after concluding **CS50x**. It took me a few months to finish it. Every time I wanted to implement a new feature I would search the net and learn a lot in the process. I really enjoyed the experience. But then, after miserably failing to deploy the app to _Heroku_ and a lot of headache, I decided to take **CS50w** so that I could eventually learn how to put something to work on the internet for real.

But I still wanted to properly finish the course, so I decided to ask the _Discord_ community if it was allowed to submit a final project like mine that runs only locally. They said it was no problem, and indeed, there are many web applications like that in the _Gallery of Final Projects_. That cheered me up to finally record a video and submit my project.

However, as I looked through my project, I realized that the design would be way much better if using _Django_, since the application deals a lot with user data, and also for organization sake. But by the time I made this project, I didn't know _Django_. And as I read each piece of code, along with the comments, it made me feel some of the thrill I felt back then, when I was learning new things and getting excited seeing things working as expected. So I decided to stay with _Flask_ and just made some slight changes to the code, improving the design, and fixing a few bugs that showed up. Regarding the templates, I bet I could do better, there must be better ways for implementing some of those features, but things were already working well. And despite a little confusion at first (second and third) glance, it really seemed to make sense, considering the amount of knowledge I had back then.

Now there is one thing that I kind of copy pasted from the **CS50** staff, which is the fancy responsive navbar made with bootstrap classes. Of course I made some changes, but the credits go for them. Also, I grabbed the _login_required_ function from them too.

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

    Handles joke voting at `/rate/<vote>` where `vote` may be either `add` or `remove`.

    If the user wants to vote for (aka like, rate or pun up) a joke, or to remove his vote, the rate function interacts with the SQLite database in order to do so. It returns the updated rating of that joke to the JS callback function as JSON, so that the rating can be visually incremented when user puns up a joke.

    Login is required.

- ### posts:

    Display all posts. A post is nothing but a joke, along with the profile picture and username of its author and it's possible comments and rating. This function interacts with the database to retrieve information from all users.
    
    By visiting `/posts/<sort_order>` this view works for two different pages in the website. Users can visit the *newest*(ordered by date) or the *phuniest*(ordered by rating) posts page.
    
    Login is required.
    
- ### comment:

    Add a comment to a given joke with id of `joke_id`. The `/comment/<joke_id>` route only accepts POST requests. It interacts with the SQL database to add the comment that the user has (hopefully!) entered as Markdown in a `textarea`.

    One interesting thing that I learned when writing this view is the `cursor.lastrowid` (where `cursor = connection.cursor()` and `connection = sqlite3.connect('phun.db')`) property. The primary key of a row in a SQL db table is autoincremented when adding new rows. And in this case, I had to pass the comment id to the JS callback function (This route is requested through an Ajax request). So the `.lastrowid` property allowed me to generate _html_ using the JS file to display the newly added comment, and let the `/delete/<stuff>` route (more on that in a bit) clearly identify it.

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

    Display a form for the user to type in his username, password, password confirmation and email address. A JS script sends info for this function via Ajax POST requests. With this info, we can identify which field is the user currently filling, so that we can give instant feedback (handled by another function, inside _helpers.py_ file).

    If any user input is not valid, the registration process won't be procced. Although instant feedback is given though POST requests, even if all inputs are valid, the registration will only be finished when the user clicks the register button.

    After signing up, user is redirected to the login page and notified through a *Flask flashed message* that the registration was successful.

- ### logout:

    Logs user out, by clearing the session. User is redirected to login page and notified that he is logged out.



## helpers.py

This file has some helper functions, called by the views in _app.py_ to perform some tasks.

- ### login_required:

    Designed by the CS50 staff, this function, when applied via _decorators_(@) to routes, redirects users to the login page when they're not logged in, that is, when their user id has not yet been added to the session.

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

    That's useful because when fetching multiple results from a SQL query you get a list o tupples, that means, each individual element of the list is a tupple. That's strange, because each tupple has only one element. Why not just return a simple list, or maybe a tupple entirely? Well, but that's how the `sqlite3` library works. But this is minimal in comparison to its simplicity for querying databases.

    This function is used to convert jokes and comments from markdown (I mean, they're only _interpreted_ as markdown, they're not stored in actual markdown files, just as text in the database) to html.

    Returns a converted list, not as a list of tupples, but as a list of lists. 😵🤪

- ### give_feedback:

    Ensure correct input and give corresponding feedback to user when filling the registration form.

    This is by far the most exciting feature I've implemented. It feels really good to see that instant feedback popping up as I type.

    The `give_feedback` function is called by the `register` view, which itself is called by an Ajax POST request coming from `feedback.js`. It receives as arguments the value of the input fields the user is submitting, such as username, password, email, or even all fields at once (as by clicking the register button), flags to identify which fields are being submitted and a bool to indicate if user is submitting the whole form or not.

    It returns a dictionary containing all feedbacks, positive or not.



## .env

It contains my *Gmail* username, used by `give_feedback` function to check email validity using the `validate_email` function from the _validate_email_ library.



## phun.db

A SQLite database to store users data. It has four tables. They are:

- comments
- jokes
- votes
- users

I did my best at designing it, trying to avoid redundancies, but surely one could do better. The `c_username` column which stands for `"commenter's username"` seems like a redundancy (and in essence, it is), but it avoids additional queries. The famous "Memory x Speed" tradeoff comes into the scene, and I chose to gain speed in trade for some memory. One thing that influenced my choice too was the complexity. I'm not so good at SQL when it comes to nesting things, so I decided to do that to avoid wasting unnecessary hours with something that could be solved by just allocating a little more memory.



## Templates

Taking advantage of _Jinja2_, Flask's templating language, I was able to avoid much redandancy, at the cost of some complexity.

- ### layout.html:

    Home of the `<head>` tag, containing all the meta information, _Bootstrap_ and _JQuery_ stuff, as well as a link to a `styles.css` file and one to a JS script for animating the dropdown icon in the navigation bar.

    The navbar was basically a copy-paste from the distribution code of ***CS50's** Problem Set 9, Finance*. Of course I customized it, but still I would have had a lot of extra work finding out how to build something like this from scratch, or studying Bootstrap classes, so the credits go all for the staff.

    This html page has a `<main>` tag whose content changes for each page visited, but all other contents of the layout are extended to the other pages (except for the `<title>`, of course, that one changes too).

- 
