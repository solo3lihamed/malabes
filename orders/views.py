from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from shop.models import Cart
from shop.views import get_or_create_cart
from .models import Order, OrderItem, ShippingInfo
import random
import string


def generate_order_number():
    """Generate unique order number"""
    timestamp = timezone.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.digits, k=6))
    return f"ORD{timestamp}{random_part}"


def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'سلة التسوق فارغة!')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=generate_order_number(),
            total_price=cart.total_price,
            notes=request.POST.get('notes', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                size=cart_item.size,
                price=cart_item.product.get_price
            )
        
        # Create shipping info
        ShippingInfo.objects.create(
            order=order,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code', ''),
            notes=request.POST.get('delivery_notes', '')
        )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'تم إنشاء طلبك بنجاح! رقم الطلب: {order.order_number} 🎉')
        return redirect('orders:order_detail', order_number=order.order_number)
    
    context = {
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


def order_detail(request, order_number):
    """Order detail and tracking"""
    order = get_object_or_404(Order, order_number=order_number)
    
    # Check if user has permission to view this order
    if order.user and request.user != order.user:
        messages.error(request, 'ليس لديك صلاحية لعرض هذا الطلب')
        return redirect('shop:home')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)
