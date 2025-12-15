from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'تم التأكيد'),
        ('processing', 'قيد التجهيز'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, verbose_name='المستخدم')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='رقم الطلب')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع الكلي')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب #{self.order_number}"

    @property
    def status_display(self):
        """Get Arabic status display"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def status_step(self):
        """Get current step number for progress tracking"""
        steps = {
            'pending': 1,
            'confirmed': 2,
            'processing': 3,
            'shipped': 4,
            'delivered': 5,
            'cancelled': 0,
        }
        return steps.get(self.status, 0)


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='الطلب')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج')
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    size = models.CharField(max_length=10, blank=True, verbose_name='المقاس')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'عنصر في الطلب'
        verbose_name_plural = 'عناصر الطلبات'

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self):
        """Calculate item subtotal"""
        return self.price * self.quantity


class ShippingInfo(models.Model):
    """Shipping and contact information for orders"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping', verbose_name='الطلب')
    full_name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
    address = models.TextField(verbose_name='العنوان')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='الرمز البريدي')
    notes = models.TextField(blank=True, verbose_name='ملاحظات التوصيل')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'معلومات الشحن'
        verbose_name_plural = 'معلومات الشحن'

    def __str__(self):
        return f"شحن الطلب #{self.order.order_number}"
