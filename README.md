# Seam

This is my submission for the Seam backend intern take-home assignment, where I created a a simple API for a blog application that allows users to manage blog posts and comments. I created two local files, posts_db.json and comments_db.json, to act as mock databases so that the API actions persist on your local machine.

Each post in posts_db.json has a postId, title, author, content, and array of comments. Each comment in comments_db.json has an id, postId, content, and author.

To run the program, first make sure python and pip are installed. Then, run:
```
pip install Flask
```

After Flask is installed, run:
```
python app.py
```
to start the server. The API can be tested using software such as Postman or Insomnia. The GET requests can be tested from the browser, but the POST requests require a separate API testing software.