"""
recommender.py — Four recommendation algorithms
  1. Content-Based  : Matches user's highly-rated genres/authors
  2. Collaborative  : User-user similarity via Jaccard on rated books
  3. Hybrid         : Weighted blend (60 % content + 40 % collab)
  4. Trending       : Most-rated + highest avg rating recently
"""

from models.book import (
    find_book_by_id, get_all_books, get_books_by_genre,
    get_top_rated, get_trending_books
)


# ────────────────────────────────────────────────
#  CONTENT-BASED
# ────────────────────────────────────────────────
def get_content_based(user, n=12):
    """Recommend books matching the user's preferred genres/authors."""
    rated = user.get('ratings', {})
    if not rated:
        return get_top_rated(n)

    liked_genres = {}
    liked_authors = {}

    for book_id, rating in rated.items():
        if rating >= 3:
            book = find_book_by_id(book_id)
            if book:
                g = book.get('genre', '')
                a = book.get('author', '')
                liked_genres[g] = liked_genres.get(g, 0) + rating
                liked_authors[a] = liked_authors.get(a, 0) + rating

    if not liked_genres:
        return get_top_rated(n)

    top_genres = sorted(liked_genres, key=liked_genres.get, reverse=True)[:3]
    top_authors = sorted(liked_authors, key=liked_authors.get, reverse=True)[:2]

    rated_ids = set(rated.keys())
    recs = []
    seen = set()

    # Books from top genres
    for genre in top_genres:
        for b in get_books_by_genre(genre, limit=10):
            bid = str(b['_id'])
            if bid not in rated_ids and bid not in seen:
                recs.append(b)
                seen.add(bid)

    # Books by top authors (from all books)
    if len(recs) < n:
        for b in get_all_books():
            bid = str(b['_id'])
            if bid not in rated_ids and bid not in seen and b.get('author', '') in top_authors:
                recs.append(b)
                seen.add(bid)

    # Pad with top-rated
    if len(recs) < n:
        for b in get_top_rated(20):
            bid = str(b['_id'])
            if bid not in rated_ids and bid not in seen and len(recs) < n:
                recs.append(b)
                seen.add(bid)

    return recs[:n]


# ────────────────────────────────────────────────
#  COLLABORATIVE FILTERING  (User-User)
# ────────────────────────────────────────────────
def get_collaborative(user, n=12):
    """
    Find users who rated similar books, then recommend
    books those neighbours loved that the current user hasn't seen.
    Uses Jaccard similarity on the set of commonly rated books.
    """
    from models.user import get_all_users

    rated = user.get('ratings', {})
    current_uid = str(user.get('_id', ''))

    if not rated:
        return get_top_rated(n)

    rated_ids = set(rated.keys())

    # Compute similarity with every other user
    neighbours = []
    all_users = get_all_users()
    for other in all_users:
        if str(other.get('_id', '')) == current_uid:
            continue
        other_rated = other.get('ratings', {})
        other_ids = set(other_rated.keys())

        # Jaccard similarity
        intersection = rated_ids & other_ids
        union = rated_ids | other_ids
        if not union:
            continue
        similarity = len(intersection) / len(union)

        if similarity > 0:
            neighbours.append((similarity, other_rated))

    # Sort by similarity desc; take top 10
    neighbours.sort(key=lambda x: x[0], reverse=True)
    top_neighbours = neighbours[:10]

    if not top_neighbours:
        return get_top_rated(n)

    # Aggregate scores from neighbours
    book_scores = {}
    for sim, their_ratings in top_neighbours:
        for bid, rating in their_ratings.items():
            if bid not in rated_ids:
                book_scores[bid] = book_scores.get(bid, 0) + sim * rating

    # Sort by score desc
    sorted_book_ids = sorted(book_scores, key=book_scores.get, reverse=True)

    recs = []
    seen = set()
    for bid in sorted_book_ids:
        if len(recs) >= n:
            break
        b = find_book_by_id(bid)
        if b and bid not in seen:
            recs.append(b)
            seen.add(bid)

    # Pad
    if len(recs) < n:
        for b in get_top_rated(n * 2):
            bid = str(b['_id'])
            if bid not in rated_ids and bid not in seen and len(recs) < n:
                recs.append(b)
                seen.add(bid)

    return recs[:n]


# ────────────────────────────────────────────────
#  HYBRID  (Content 60 % + Collaborative 40 %)
# ────────────────────────────────────────────────
def get_hybrid(user, n=12):
    """
    Blend content-based and collaborative scores.
    Uses position-based scoring so no rescaling needed.
    """
    content = get_content_based(user, n=n * 2)
    collab  = get_collaborative(user, n=n * 2)

    # Assign a score: books ranked higher get a bigger score
    def rank_scores(book_list, weight):
        scores = {}
        total = len(book_list)
        for i, b in enumerate(book_list):
            bid = str(b['_id'])
            scores[bid] = scores.get(bid, 0) + weight * (total - i)
        return scores

    content_scores = rank_scores(content, 0.6)
    collab_scores  = rank_scores(collab,  0.4)

    all_ids = set(content_scores) | set(collab_scores)
    combined = {bid: content_scores.get(bid, 0) + collab_scores.get(bid, 0)
                for bid in all_ids}

    sorted_ids = sorted(combined, key=combined.get, reverse=True)

    rated_ids = set(user.get('ratings', {}).keys())
    recs = []
    seen = set()
    for bid in sorted_ids:
        if len(recs) >= n:
            break
        if bid not in rated_ids and bid not in seen:
            b = find_book_by_id(bid)
            if b:
                recs.append(b)
                seen.add(bid)

    # Pad with top-rated if needed
    if len(recs) < n:
        for b in get_top_rated(n * 2):
            bid = str(b['_id'])
            if bid not in rated_ids and bid not in seen and len(recs) < n:
                recs.append(b)
                seen.add(bid)

    return recs[:n]


# ────────────────────────────────────────────────
#  TRENDING
# ────────────────────────────────────────────────
def get_trending(n=12):
    """Books sorted by rating count, then avg rating (no user context needed)."""
    return get_trending_books(limit=n)


# ────────────────────────────────────────────────
#  LEGACY ALIAS  (keeps old call-sites working)
# ────────────────────────────────────────────────
def get_recommendations(user, n=12):
    return get_hybrid(user, n=n)
