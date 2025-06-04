from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CulturalItem, UserSwipe
from django.db.models import Exists, OuterRef

@login_required
def swipe_view(request):
    current_user = request.user

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action') # 'like' or 'dislike'

        item = get_object_or_404(CulturalItem, id=item_id)

        if action in ['like', 'dislike']:
            liked = (action == 'like')
            UserSwipe.objects.update_or_create(
                user=current_user,
                item=item,
                defaults={'liked': liked}
            )
        return redirect('swipe_view') # Redirect to get the next item

    # Find next item to swipe: one that the user hasn't swiped yet.
    # Subquery to find items the user has already swiped
    swiped_items_subquery = UserSwipe.objects.filter(
        user=current_user,
        item=OuterRef('pk')
    )

    # Select an item that does not have an existing swipe record for the current user
    next_item = CulturalItem.objects.annotate(
        has_swiped=Exists(swiped_items_subquery)
    ).filter(has_swiped=False).order_by('?').first() # Order by '?' for random, or use e.g. 'created_at'

    if not next_item:
        # No more items to swipe or all items have been swiped by the user
        return render(request, 'swipe/swipe_done.html')

    context = {
        'item': next_item,
    }
    return render(request, 'swipe/swipe_item.html', context)
