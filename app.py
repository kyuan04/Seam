import os
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# file paths for temp db's
posts_db_file = 'posts_db.json'
comments_db_file = 'comments_db.json'

# loads data from a JSON file
# will be used to load data posts_db.json and comments_db.json
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

# saves data to a JSON file
# will be used to write to posts_db.json and comments_db.json
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# load posts and comments
posts_db = load_data(posts_db_file)
comments_db = load_data(comments_db_file)


@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'


@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(list(posts_db)), 200


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    # get the first post in posts_db with id
    post = next((post for post in posts_db if post['postId'] == id), None) 
    if post is None:
        return '<h1>Post with specified ID not found. Try again.</h1>', 404
    return jsonify(post), 200


@app.route('/posts', methods=['POST'])
def create_post():
    # handle bad request
    if not request.json or not 'title' in request.json or not 'content' in request.json or not 'author' in request.json:
        return '<h1>Must include a title, author, and content body.</h1>', 400

    new_post = {
        'postId': posts_db[-1]['postId'] + 1 if posts_db else 1, # increment postId as posts are added
        'title': request.json['title'],
        'content': request.json['content'],
        'author': request.json['author'],
        'comments': []
    }

    posts_db.append(new_post)
    save_data(posts_db_file, posts_db)
    return jsonify(new_post), 201


@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # handle bad request
    if not request.json:
        return '<h1>Include an updated title, author, or content body.</h1>', 400

    # get the first post in posts_db with id
    post = next((post for post in posts_db if post['postId'] == id), None)
    if post is None:
        return '<h1>Post with specified ID not found. Try again. If you wish to create a post, send POST request to 127.0.0.1:5000/posts.</h1>', 404

    # update the post's information
    # if request doesn't specify new value for a field, keep old value for that field.
    post['title'] = request.json.get('title', post['title'])
    post['content'] = request.json.get('content', post['content'])
    post['author'] = request.json.get('author', post['author'])
    save_data(posts_db_file, posts_db)
    return jsonify(post), 200


@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # get the first post in posts_db with id
    post = next((post for post in posts_db if post['postId'] == id), None)
    if post is None:
        return '<h1>Post with specified ID not found. Try again.</h1>', 404

    posts_db.remove(post)
    save_data(posts_db_file, posts_db)
    return f'<h1>Post {id} successfully deleted.</h1>', 200


@app.route('/posts/<int:postId>/comments', methods=['GET'])
def get_comments(postId):
    # get the first post in posts_db with postId
    post = next((post for post in posts_db if post['postId'] == postId), None)
    if post is None:
        return '<h1>Post with specified ID not found. Try again.</h1>', 404

    return jsonify(post['comments']), 200

@app.route('/posts/<int:postId>/comments', methods=['POST'])
def create_comment(postId):
    if not request.json or not 'content' in request.json or not 'author' in request.json:
        return '<h1>Must include content and author</h1>', 400

    # get the first post in posts_db with postId
    post = next((post for post in posts_db if post['postId'] == postId), None)
    if post is None:
        return '<h1>Post with specified ID not found. Try again.</h1>', 404

    new_comment = {
        'id': comments_db[-1]['id'] + 1 if comments_db else 1,
        'postId': postId,
        'content': request.json['content'],
        'author': request.json['author']
    }

    comments_db.append(new_comment)
    save_data(comments_db_file, comments_db)
    posts_db[posts_db.index(post)]['comments'].append(new_comment)
    save_data(posts_db_file, posts_db)

    return jsonify(new_comment), 201

if __name__ == '__main__':
    app.run(debug=True)
