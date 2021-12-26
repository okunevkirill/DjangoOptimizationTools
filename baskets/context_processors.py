def basket(request):
    """User basket formation function"""
    user_baskets = []
    if request.user.is_authenticated:
        user_baskets = request.user.basket.all()

    return {
        'baskets': user_baskets,
    }
