from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import calculate_match_score

@login_required
def match_list_view(request):
    current_user = request.user
    users = User.objects.exclude(id=current_user.id).exclude(is_staff=True).exclude(is_superuser=True) # Exclude self and admin users

    matches = []
    for user in users:
        score, common_items = calculate_match_score(current_user, user)
        if score > 0: # Only show users with some level of match
            matches.append({
                'user': user,
                'score': score,
                'common_items': common_items,
            })

    # Sort matches by score, descending
    matches.sort(key=lambda x: x['score'], reverse=True)

    context = {
        'matches': matches,
    }
    return render(request, 'matcher/match_list.html', context)
