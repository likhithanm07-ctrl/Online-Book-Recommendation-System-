from datetime import datetime
from database.db import get_collection
from bson import ObjectId

def get_feedbacks_collection():
    return get_collection('feedbacks')

def get_books():
    return get_collection('books')

def create_book(title, author, genre, description, cover_url='', year=None, isbn=''):
    book = {
        'title': title,
        'author': author,
        'genre': genre,
        'description': description,
        'cover_url': cover_url,
        'year': year,
        'isbn': isbn,
        'ratings': [],       # list of {user_id, rating}
        'avg_rating': 0.0,
        'created_at': datetime.utcnow()
    }
    result = get_books().insert_one(book)
    book['_id'] = result.inserted_id
    return book

def find_book_by_id(book_id):
    try:
        return get_books().find_one({'_id': ObjectId(book_id)})
    except Exception:
        return None

def get_all_books():
    return list(get_books().find())

def search_books(query):
    regex = {'$regex': query, '$options': 'i'}
    return list(get_books().find({
        '$or': [
            {'title': regex},
            {'author': regex},
            {'genre': regex},
            {'description': regex}
        ]
    }))

def add_rating(book_id, user_id, rating):
    book = find_book_by_id(book_id)
    if not book:
        return
    # Remove old rating from this user if exists
    ratings = [r for r in book.get('ratings', []) if r['user_id'] != user_id]
    ratings.append({'user_id': user_id, 'rating': rating})
    avg = sum(r['rating'] for r in ratings) / len(ratings) if ratings else 0
    get_books().update_one(
        {'_id': ObjectId(book_id)},
        {'$set': {'ratings': ratings, 'avg_rating': round(avg, 1)}}
    )

def delete_book(book_id):
    get_books().delete_one({'_id': ObjectId(book_id)})

def update_book(book_id, data):
    get_books().update_one({'_id': ObjectId(book_id)}, {'$set': data})

def get_books_by_genre(genre, limit=10):
    return list(get_books().find({'genre': {'$regex': genre, '$options': 'i'}}).limit(limit))

def get_top_rated(limit=10):
    return list(get_books().find().sort('avg_rating', -1).limit(limit))

def get_trending_books(limit=12):
    """
    Trending = most frequently rated books, tie-broken by avg_rating.
    We use the MongoDB aggregation pipeline so we can sort by the
    computed length of the 'ratings' array.
    """
    pipeline = [
        {
            '$addFields': {
                'rating_count': {'$size': {'$ifNull': ['$ratings', []]}}
            }
        },
        {
            '$sort': {'rating_count': -1, 'avg_rating': -1}
        },
        {
            '$limit': limit
        }
    ]
    return list(get_books().aggregate(pipeline))

def add_feedback(book_id, user_id, username, feedback_text):
    """Add a user review/feedback for a book."""
    feedback = {
        'book_id': book_id,
        'user_id': user_id,
        'username': username,
        'text': feedback_text.strip(),
        'created_at': datetime.utcnow()
    }
    get_feedbacks_collection().insert_one(feedback)
    return feedback

def get_feedbacks(book_id):
    """Get all feedbacks for a given book, newest first."""
    return list(
        get_feedbacks_collection()
        .find({'book_id': book_id})
        .sort('created_at', -1)
    )
