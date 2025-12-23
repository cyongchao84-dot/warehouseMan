from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """产品实体"""
    CATEGORY_CHOICES = [
        ('electronics', '电子产品'),
        ('clothing', '服装'),
        ('food', '食品'),
        ('tools', '工具'),
        ('other', '其他'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="产品名称")
    description = models.TextField(blank=True, verbose_name="描述")
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='other',
        verbose_name="类别"
    )
    quantity = models.IntegerField(default=0, verbose_name="库存数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    location = models.CharField(max_length=100, verbose_name="存放位置")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"
        permissions = [
            ("can_view_product", "可以查看产品"),
            ("can_add_product", "可以添加产品"),
            ("can_change_product", "可以修改产品"),
            ("can_delete_product", "可以删除产品"),
            ("can_search_product", "可以搜索产品"),
        ]
    
    def __str__(self):
        return f"{self.name} (库存: {self.quantity})"