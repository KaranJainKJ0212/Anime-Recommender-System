# from flask import Flask, request, render_template, redirect, url_for, jsonify
# import pandas as pd
# import numpy as np
# import pickle

# app = Flask(__name__)

# # Load the preprocessed data and similarity matrix
# with open('preprocessed_data.pkl', 'rb') as f:
#     new_df = pickle.load(f)
# with open('similarity_matrix.pkl', 'rb') as f:
#     similarity = pickle.load(f)

# def recommend(anime, sort_by=None, order='asc', filter_genre=None):
#     if anime not in new_df['Name'].values:
#         return None

#     anime_index = new_df[new_df['Name'] == anime].index[0]
#     distances = similarity[anime_index]
#     anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommendations = []

#     for i in anime_list:
#         row = new_df.iloc[i[0]]
#         if filter_genre and filter_genre not in row['Genres']:
#             continue
#         recommendations.append({
#             'Name': row['Name'],
#             'Genres': ', '.join(row['Genres']),
#             'Episodes': row['Episodes'],
#             'Score': row['Score'],
#             'Type': row['Type'],
#             'Rating': row['Rating'],
#             'Links': row['Links']
#         })

#     if sort_by and sort_by != 'Genres':
#         recommendations = sorted(recommendations, key=lambda x: float(x[sort_by]) if x[sort_by] != 'UNKNOWN' else float('inf'), reverse=(order == 'desc'))

#     available_genres = sorted(set(genre for rec in recommendations for genre in rec['Genres'].split(', ')))

#     return recommendations, available_genres

# @app.route('/')
# def home():
#     return render_template('index01.html')

# @app.route('/recommend', methods=['POST'])
# def get_recommendations():
#     anime_name = request.form['anime_name']
#     return redirect(url_for('show_recommendations', anime_name=anime_name))

# @app.route('/recommendations/<anime_name>')
# def show_recommendations(anime_name):
#     sort_by = request.args.get('sort_by')
#     order = request.args.get('order', 'asc')
#     filter_genre = request.args.get('filter_genre')
#     recommendations, available_genres = recommend(anime_name, sort_by=sort_by, order=order, filter_genre=filter_genre)
#     return render_template('recommendations.html', recommendations=recommendations, anime_name=anime_name, sort_by=sort_by, order=order, available_genres=available_genres, filter_genre=filter_genre)

# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('query', '')
#     results = new_df[new_df['Name'].str.contains(query, case=False, na=False)]['Name'].tolist()
#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=7860, debug=True)



# from flask import Flask, request, render_template, redirect, url_for, jsonify, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import pandas as pd
# import numpy as np
# import pickle
# import os

# app = Flask(__name__)
# app.secret_key = os.urandom(24)  # For session management

# # Database setup
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# # Initialize database tables
# def create_tables():
#     with app.app_context():
#         db.create_all()

# create_tables()

# # Load the preprocessed data and similarity matrix
# with open('preprocessed_data.pkl', 'rb') as f:
#     new_df = pickle.load(f)
# with open('similarity_matrix.pkl', 'rb') as f:
#     similarity = pickle.load(f)

# def recommend(anime, sort_by=None, order='asc', filter_genre=None):
#     if anime not in new_df['Name'].values:
#         return None

#     anime_index = new_df[new_df['Name'] == anime].index[0]
#     distances = similarity[anime_index]
#     anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommendations = []

#     for i in anime_list:
#         row = new_df.iloc[i[0]]
#         if filter_genre and filter_genre not in row['Genres']:
#             continue
#         recommendations.append({
#             'Name': row['Name'],
#             'Genres': ', '.join(row['Genres']),
#             'Episodes': row['Episodes'],
#             'Score': row['Score'],
#             'Type': row['Type'],
#             'Rating': row['Rating'],
#             'Links': row['Links']
#         })

#     if sort_by and sort_by != 'Genres':
#         recommendations = sorted(recommendations, key=lambda x: float(x[sort_by]) if x[sort_by] != 'UNKNOWN' else float('inf'), reverse=(order == 'desc'))

#     available_genres = sorted(set(genre for rec in recommendations for genre in rec['Genres'].split(', ')))

#     return recommendations, available_genres

# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return redirect(url_for('index'))
#     return redirect(url_for('login'))

# @app.route('/index')
# def index():
#     return render_template('index01.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             return redirect(url_for('index'))
#         flash('Invalid credentials or User not found')
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user:
#             flash('User already exists')
#         else:
#             hashed_password = generate_password_hash(password, method='sha256')
#             new_user = User(username=username, password=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('User registered successfully! Please log in.')
#             return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)  # Remove the user_id from the session
#     flash('You have been logged out.')
#     return redirect(url_for('login'))


# @app.route('/recommend', methods=['POST'])
# def get_recommendations():
#     anime_name = request.form['anime_name']
#     return redirect(url_for('show_recommendations', anime_name=anime_name))

# @app.route('/recommendations/<anime_name>')
# def show_recommendations(anime_name):
#     sort_by = request.args.get('sort_by')
#     order = request.args.get('order', 'asc')
#     filter_genre = request.args.get('filter_genre')
#     recommendations, available_genres = recommend(anime_name, sort_by=sort_by, order=order, filter_genre=filter_genre)
#     return render_template('recommendations.html', recommendations=recommendations, anime_name=anime_name, sort_by=sort_by, order=order, available_genres=available_genres, filter_genre=filter_genre)

# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('query', '')
#     results = new_df[new_df['Name'].str.contains(query, case=False, na=False)]['Name'].tolist()
#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=7860, debug=True)


from flask import Flask, request, render_template, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import pickle
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_name = db.Column(db.String(200), nullable=False)

# Initialize database tables
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Load the preprocessed data and similarity matrix
with open('preprocessed_data.pkl', 'rb') as f:
    new_df = pickle.load(f)
with open('similarity_matrix.pkl', 'rb') as f:
    similarity = pickle.load(f)

def recommend(anime, sort_by=None, order='asc', filter_genre=None):
    if anime not in new_df['Name'].values:
        return None

    anime_index = new_df[new_df['Name'] == anime].index[0]
    distances = similarity[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommendations = []

    for i in anime_list:
        row = new_df.iloc[i[0]]
        if filter_genre and filter_genre not in row['Genres']:
            continue
        recommendations.append({
            'Name': row['Name'],
            'Genres': ', '.join(row['Genres']),
            'Episodes': row['Episodes'],
            'Score': row['Score'],
            'Type': row['Type'],
            'Rating': row['Rating'],
            'Links': row['Links']
        })

    if sort_by and sort_by != 'Genres':
        recommendations = sorted(recommendations, key=lambda x: float(x[sort_by]) if x[sort_by] != 'UNKNOWN' else float('inf'), reverse=(order == 'desc'))

    available_genres = sorted(set(genre for rec in recommendations for genre in rec['Genres'].split(', ')))

    return recommendations, available_genres

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index01.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Invalid credentials or User not found')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully! Please log in.')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user_id from the session
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    anime_name = request.form['anime_name']
    return redirect(url_for('show_recommendations', anime_name=anime_name))

@app.route('/recommendations/<anime_name>')
def show_recommendations(anime_name):
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    filter_genre = request.args.get('filter_genre')
    recommendations, available_genres = recommend(anime_name, sort_by=sort_by, order=order, filter_genre=filter_genre)
    return render_template('recommendations.html', recommendations=recommendations, anime_name=anime_name, sort_by=sort_by, order=order, available_genres=available_genres, filter_genre=filter_genre)

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if 'user_id' not in session:
        return jsonify({'message': 'Please log in to add to watchlist'}), 401

    data = request.get_json()
    anime_name = data['anime_name']
    
    # Check if anime is already in the watchlist
    existing_entry = Watchlist.query.filter_by(user_id=session['user_id'], anime_name=anime_name).first()
    if existing_entry:
        return jsonify({'message': 'Already in Watchlist'})
    
    new_entry = Watchlist(user_id=session['user_id'], anime_name=anime_name)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({'message': 'Added to Watchlist'})

@app.route('/watchlist')
def watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    watchlist_items = Watchlist.query.filter_by(user_id=session['user_id']).all()
    return render_template('watchlist.html', watchlist_items=watchlist_items)



@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = new_df[new_df['Name'].str.contains(query, case=False, na=False)]['Name'].tolist()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)


