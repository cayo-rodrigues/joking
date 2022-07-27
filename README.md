# JOKING

## Video Demonstration

https://drive.google.com/file/d/1WlDjifUOROhicYQ62elW9S6AlMDdtWDM/view?usp=sharing

---

## General

JoKing is a social network for sharing <s>bad</s> puns. Users can see their profile, upload profile pictures (`jpg`, `png` or even `gifs`), share their own jokes, like and comment other's jokes and see other user's profile pages.

It is built on top of `Python` and `Flask`, using `SQLite` for the database. Profile pictures are stored in the filesystem. The frontend side of the application was developed using `HTML`, `CSS`, `Javascript`, `Bootstrap` and `JQuery`. Also, `Jinja2` is used as a templating engine.

## Background

This project was developed as a Final Project for [CS50X](https://cs50.harvard.edu/x/2021/). I began to work on this project shortly after concluding the course. I remember that I had a really great time working on this. Everyday I would have to search the net looking for how to implement some new feature, and I learned really **a lot** in the proccess. I mean, that's one of the things that the course taught me, to teach my self. It took me quite a while to finish it.

Back then, I tried but I just couldn't deploy it to **Heroku**. Maybe I just didn't have the maturity I have now to read error logs :joy:. But anyway, now (2022-07-27), I decided to take this project one step further. Finally, after some major debbuging, JoKing is live on the internet!

Since this project is hosted by **Heroku**, and it is using `SQLite`, all new info desappear each 24 hours. Back then I didn't know about `PostgreSQL` (or any other database system that work as a server) or how to use it, and since this project is not meant to be a social network for real, I decided to stay with `SQLite`.

## Final Thoughts

Yeah, if you look at the source code, you're gonna see how much it could be better. Such a poor organization, indeed, I agree. Also the commits, they're just awful, not even close to conventional commits. Maybe the database tables could be better designed in some ways too. And no doubt `app.py` and `helpers.py` modules are overloaded, they could surely be broken into smaller modules and/or packages.

But looking back, considering the amount of knowledge I had back then, and my former naiveness, this project is really a great milestone. It is my first full stack project. So I am really happy to see that it works so well, despite this little lack of good practices.

Sure, there are some things that could possibly be added, such as a "forgot my password" feature, a way for users to edit their personal info, a friendship system and so on. Also I think it'd be cool to maybe have some way to track how many likes users have in total, and create a page to display the top rated ones, then whoever would be the first, would become the Jo**King**.

## Credits

The amazing **CS50 staff** must be credited for the fancy responsive navbar made with bootstrap classes. Althogh I made some changes, it is clear that it's got the same base as the navbar used in **Problem Set 9, Finance**. Besides that, I grabbed the `login_required` function from them too.