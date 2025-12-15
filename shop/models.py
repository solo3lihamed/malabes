from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Product categories: clothing, shoes, accessories"""
    name = models.CharField(max_length=100, verbose_name='الاسم')
    slug = models.SlugField(unique=True, verbose_name='الرابط')
    icon = models.CharField(max_length=50, default='🛍️', verbose_name='الأيقونة')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Product model for all items"""
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='الفئة')
    name = models.CharField(max_length=200, verbose_name='الاسم')
    slug = models.SlugField(unique=True, verbose_name='الرابط')
    description = models.TextField(verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='سعر الخصم')
    image = models.ImageField(upload_to='products/', verbose_name='الصورة الرئيسية')
    stock = models.PositiveIntegerField(default=0, verbose_name='المخزون')
    available_sizes = models.CharField(max_length=200, blank=True, verbose_name='المقاسات المتاحة')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    is_featured = models.BooleanField(default=False, verbose_name='مميز')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        """Return discount price if available, otherwise regular price"""
        return self.discount_price if self.discount_price else self.price

    @property
    def has_discount(self):
        """Check if product has a discount"""
        return self.discount_price is not None and self.discount_price < self.price


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='المنتج')
    image = models.ImageField(upload_to='products/', verbose_name='الصورة')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'صورة منتج'
        verbose_name_plural = 'صور المنتجات'

    def __str__(self):
        return f"صورة {self.product.name}"


class Cart(models.Model):
    """Shopping cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='المستخدم')
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name='مفتاح الجلسة')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سلة تسوق'
        verbose_name_plural = 'سلات التسوق'

    def __str__(self):
        if self.user:
            return f"سلة {self.user.username}"
        return f"سلة {self.session_key}"

    @property
    def total_price(self):
        """Calculate total cart price"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Count total items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='السلة')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج')
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    size = models.CharField(max_length=10, blank=True, verbose_name='المقاس')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'عنصر في السلة'
        verbose_name_plural = 'عناصر السلة'

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self):
        """Calculate item subtotal"""
        return self.product.get_price * self.quantity
