from django.contrib.auth.models import User
from profiles.models import Profile
from swipe.models import UserSwipe, CulturalItem
import re

def _parse_text_field(text):
    if not text:
        return set()
    # Normalize: lowercase, strip whitespace, split by comma, filter empty strings
    items = [item.strip().lower() for item in re.split(r'\s*,\s*', text) if item.strip()]
    return set(items)

def calculate_questionnaire_similarity(profile1, profile2):
    common_items = []
    score = 0

    prefs1_books = _parse_text_field(profile1.favorite_books)
    prefs2_books = _parse_text_field(profile2.favorite_books)
    common_books = list(prefs1_books.intersection(prefs2_books))
    score += len(common_books) * 2 # Weight common books higher
    common_items.extend(common_books)

    prefs1_movies = _parse_text_field(profile1.favorite_movies)
    prefs2_movies = _parse_text_field(profile2.favorite_movies)
    common_movies = list(prefs1_movies.intersection(prefs2_movies))
    score += len(common_movies) * 2 # Weight common movies higher
    common_items.extend(common_movies)

    prefs1_music = _parse_text_field(profile1.favorite_music_genres)
    prefs2_music = _parse_text_field(profile2.favorite_music_genres)
    common_music = list(prefs1_music.intersection(prefs2_music))
    score += len(common_music) * 1 # Weight music genres
    common_items.extend(common_music)

    # Max possible score from questionnaire:
    # Assume avg 5 items per category, 3 categories. 5*2 + 5*2 + 5*1 = 25. This is a rough estimate.
    # For normalization, we need a more defined max score or use a different approach.
    # Let's define a max expected common items for normalization, e.g., 10 total items * weight of 2 = 20-25
    # For now, this score is raw. Normalization will be tricky without defined list sizes.
    return score, list(set(common_items)) # list(set()) to remove duplicates from different categories

def calculate_swipe_similarity(user1, user2):
    user1_likes = set(UserSwipe.objects.filter(user=user1, liked=True).values_list('item_id', flat=True))
    user2_likes = set(UserSwipe.objects.filter(user=user2, liked=True).values_list('item_id', flat=True))

    common_liked_item_ids = user1_likes.intersection(user2_likes)
    score = len(common_liked_item_ids) * 3 # Weight common swipes higher

    common_liked_items = CulturalItem.objects.filter(id__in=common_liked_item_ids).values_list('title', flat=True)

    # Max possible score: e.g., if there are 20 cultural items, max score is 20 * 3 = 60
    return score, list(common_liked_items)

def calculate_match_score(user1, user2):
    try:
        profile1 = Profile.objects.get(user=user1)
        profile2 = Profile.objects.get(user=user2)
    except Profile.DoesNotExist:
        return 0, [], [] # One of the users doesn't have a profile

    q_score, q_common = calculate_questionnaire_similarity(profile1, profile2)
    s_score, s_common = calculate_swipe_similarity(user1, user2)

    total_score = q_score + s_score
    all_common_items = list(set(q_common + s_common)) # Combine and unique

    # Normalization to 0-100:
    # This is a placeholder. Max scores need to be better defined.
    # Max questionnaire score (rough estimate): 5 books * 2 + 5 movies * 2 + 5 music * 1 = 25
    # Max swipe score (e.g., 10 shared likes * 3 = 30)
    # Max possible raw score: ~55
    # If total_score is 55, it's 100%. If 0, it's 0%.
    # For MVP, let's cap at 100 if it exceeds, and scale roughly.
    # A more robust way is to define max possible for each part.
    # Max possible q_score (e.g. 15 items * avg weight 1.66 = 25)
    # Max possible s_score (e.g. 10 items * 3 = 30)
    # Total max = 55
    # Percentage = (total_score / 55) * 100

    # Simplified normalization for MVP:
    # Let's assume a max combined raw score of (e.g. 50 for a "perfect" match based on current weighting)
    # This makes the percentage somewhat arbitrary without hard limits on number of items.
    # A better MVP approach might be to rank users by raw score and not show a percentage,
    # or show a "relative strength" indicator.
    # For now, let's try a simple scaling.
    normalized_score = min((total_score / 50.0) * 100, 100) if total_score > 0 else 0

    return int(normalized_score), all_common_items[:3] # Return score and first 3 common items
