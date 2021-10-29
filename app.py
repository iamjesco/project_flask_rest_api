from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tempdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from schemas import Post


@app.get('/api/posts/')
def get_posts():
	response = []
	for post in Post.query.all():
		response.append({
			'id': post.id,
			'title': post.title,
			'body': post.body,
			'author': post.author,
			'created': post.created
		})
	return jsonify(response)


@app.post('/api/posts/')
def create_post():
	data = request.get_json()
	payload = Post(
		title=data['title'],
		body=data['body']
	)
	try:
		db.session.add(payload)
		db.session.commit()
		return jsonify({'message': 'New post created successfully'}), 201
	except IntegrityError:
		db.session.rollback()
		return {'message': 'Duplicate post title found!'}, 409


@app.get('/api/posts/<int:pk>')
def get_post(pk):
	post = Post.query.get_or_404(pk)
	response = {
		'id': post.id,
		'title': post.title,
		'body': post.body,
		'author': post.author,
		'created': post.created
	}
	return jsonify(response)


@app.patch('/api/posts/<int:pk>')
def update_post(pk):
	return {'devs': f'{pk} updated!'}


@app.delete('/api/posts/<int:pk>')
def delete_post(pk):
	return {'devs': f'{pk} deleted!'}


if __name__ == '__main__':
	app.run()

