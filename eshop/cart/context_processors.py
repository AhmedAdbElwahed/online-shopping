from .cart import Cart


def cart(request):
    processor = {
        'cart': Cart(request),
    }
    return processor
