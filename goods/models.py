# goods/models.py
from django.db import models
from django.contrib.auth.models import User


class Goods(models.Model):
    """商品模型"""

    MAJOR_CHOICES = [
        ('advertising', 'Advertising'),
        ('animation', 'Animation'),
        ('3d_animation', '3D Animation and Visual Effects'),
        ('comics', 'Comics'),
        ('design', 'Design'),
        ('film', 'Film'),
        ('fine_arts', 'Fine Arts'),
        ('illustration', 'Illustration'),
        ('photography', 'Photography & Video'),
        ('visual_studies', 'Visual and Critical Studies'),
        ('art_history', 'Art History'),
        ('humanities', 'Humanities and Sciences'),
        ('others', 'Others'),
    ]

    CATEGORY_CHOICES = [
        ('paints', 'Paints'),
        ('brushes', 'Brushes'),
        ('papers', 'Papers/Canvas'),
        ('tools', 'Tools'),
        ('mediums', 'Mediums'),
        ('markers', 'Markers/Ink'),
        ('pencils', 'Pencils'),
        ('pastels', 'Pastels'),
        ('modeling', 'Modeling'),
        ('textbook', 'Textbook'),
        ('filming', 'Filming Device'),
        ('electronic', 'Electronic Device'),
    ]

    PAYMENT_CHOICES = [
        ('venmo', 'Venmo'),
        ('cash', 'Cash'),
        ('zelle', 'Zelle'),
        ('paypal', 'PayPal'),
        ('apple_pay', 'Apple Pay'),
    ]

    # 基础信息 (原有字段)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # 卖家信息
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    # 新增字段
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES, blank=True)
    professor = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    course_code = models.CharField(max_length=50, blank=True, help_text="e.g., DSD-3003-B")

    # 详细信息
    amount_usage = models.TextField(blank=True, help_text="Amount and usage information")
    payment_methods = models.CharField(max_length=200, blank=True, help_text="Comma-separated payment methods")
    additional_info = models.TextField(blank=True)

    # Outcome说明
    outcome_description = models.TextField(blank=True, help_text="Description for outcome images")

    # 卖家信息 (可选,如果需要关联用户)
    # seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """商品主图 (最多3张)"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='goods_images/')
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.goods.name} - Image {self.order}"


class OutcomeImage(models.Model):
    """Outcome作品图 (最多5张)"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='outcomes')
    image = models.ImageField(upload_to='outcome_images/')
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order']
        verbose_name = "Outcome Image"
        verbose_name_plural = "Outcome Images"

    def __str__(self):
        return f"{self.goods.name} - Outcome {self.order}"