from datetime import datetime
from database.db import get_collection
from bson import ObjectId

def get_users():
    return get_collection('users')

def create_user(username, email, password_hash, role='user',
                security_question='', security_answer=''):
    user = {
        'username': username,
        'email': email,
        'password': password_hash,
        'role': role,
        'created_at': datetime.utcnow(),
        'ratings': {},                    # book_id -> rating
        'favorites': [],                  # list of book_ids
        'security_question': security_question,
        'security_answer': security_answer.strip().lower(),
    }
    result = get_users().insert_one(user)
    user['_id'] = result.inserted_id
    return user

def find_user_by_email(email):
    return get_users().find_one({'email': email})

def find_user_by_username(username):
    return get_users().find_one({'username': username})

def find_user_by_id(user_id):
    try:
        return get_users().find_one({'_id': ObjectId(user_id)})
    except Exception:
        return None

def update_user_rating(user_id, book_id, rating):
    get_users().update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {f'ratings.{book_id}': rating}}
    )

def delete_user(user_id):
    get_users().delete_one({'_id': ObjectId(user_id)})

def get_all_users():
    return list(get_users().find({'role': 'user'}))

def update_user_password(user_id, new_password_hash):
    """Replace a user's hashed password."""
    get_users().update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'password': new_password_hash}}
    )

def get_security_question(email):
    """Return the security question for a given email, or None."""
    user = get_users().find_one({'email': email}, {'security_question': 1})
    if user:
        return user.get('security_question', '')
    return None
