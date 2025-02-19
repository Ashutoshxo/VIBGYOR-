from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PerformanceReviewForm
from .models import PerformanceReview
from employee.models import Employe_User

@login_required
def add_review(request):
    try:
        if isinstance(request.user, Employe_User):
            user = request.user
        else:
            user = Employe_User.objects.get(username=request.user.username)

        if request.method == 'POST':
            form = PerformanceReviewForm(request.POST, user=user)
            if form.is_valid():
                # Ensure reviewed_by is set to the logged-in user
                performance_review = form.save(commit=False)
                performance_review.reviewed_by = user  # Set the user who is submitting the review
                performance_review.save()  # Now save the review
                return redirect('performance_management:review_list')  # Redirect to the review list page
        else:
            form = PerformanceReviewForm(user=user)

        return render(request, 'performance_management/add_review.html', {'form': form})

    except Employe_User.DoesNotExist:
        # If user not found, handle the exception and show an error page
        return render(request, 'error.html', {'message': 'User not found'})


@login_required
def review_list(request):
    reviews = PerformanceReview.objects.filter(status=True)  # Retrieve reviews with status True
    has_change_permission = request.user.has_perm("performance_management.change_performancereview")
    has_delete_permission = request.user.has_perm("performance_management.delete_performancereview")

    return render(request, 'performance_management/review_list.html', {
        'reviews': reviews,
        'has_change_permission': has_change_permission,
        'has_delete_permission': has_delete_permission,
    })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    if request.user.is_superuser or request.user.has_perm('performance_management.change_performancereview'):
        if request.method == 'POST':
            form = PerformanceReviewForm(request.POST, instance=review, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('performance_management:review_list')
        else:
            form = PerformanceReviewForm(instance=review, user=request.user)
        return render(request, 'performance_management/edit_review.html', {'form': form, 'review': review})
    else:
        return redirect('permission_denied')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    review.status = False  # Mark as deleted (soft delete)
    review.save()
    return redirect('performance_management:review_list')
