import os
import sys
import django
import random

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warehouse_project.settings')
django.setup()

from django.contrib.auth.models import User
from warehouse.models import Product

def create_test_products():
    """创建测试产品数据"""
    
    print("=" * 60)
    print("开始创建测试产品数据")
    print("=" * 60)
    
    # 获取管理员用户
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.first()
    
    test_products = [
        {
            'name': '笔记本电脑 Dell XPS',
            'description': '高性能笔记本电脑，16GB内存，1TB SSD，适合编程和设计工作',
            'category': 'electronics',
            'quantity': 25,
            'price': 8999.99,
            'location': 'A区-01架-03层',
        },
        {
            'name': '纯棉T恤衫',
            'description': '100%纯棉短袖T恤，多种颜色可选，夏季必备',
            'category': 'clothing',
            'quantity': 150,
            'price': 89.99,
            'location': 'B区-03架-01层',
        },
        {
            'name': '瑞士黑巧克力',
            'description': '进口黑巧克力，72%可可含量，独立小包装',
            'category': 'food',
            'quantity': 80,
            'price': 45.50,
            'location': 'C区-冷藏02柜',
        },
        {
            'name': '多功能充电式电钻',
            'description': '家用DIY工具，20V锂电池，多种钻头套装',
            'category': 'tools',
            'quantity': 15,
            'price': 299.00,
            'location': 'D区-工具柜-02号',
        },
        {
            'name': '智能手机 iPhone 14',
            'description': '256GB存储，6.1英寸屏幕，最新iOS系统',
            'category': 'electronics',
            'quantity': 8,
            'price': 6999.00,
            'location': 'A区-02架-01层',
        },
        {
            'name': '蓝色牛仔裤',
            'description': '经典蓝色牛仔裤，直筒款，多尺寸可选',
            'category': 'clothing',
            'quantity': 45,
            'price': 199.99,
            'location': 'B区-01架-02层',
        },
        {
            'name': '有机燕麦片',
            'description': '无添加有机燕麦，早餐健康食品',
            'category': 'food',
            'quantity': 120,
            'price': 32.80,
            'location': 'C区-常温01柜',
        },
        {
            'name': '工具箱套装',
            'description': '128件工具套装，家用维修必备',
            'category': 'tools',
            'quantity': 30,
            'price': 159.00,
            'location': 'D区-工具柜-01号',
        },
    ]
    
    created_count = 0
    for product_data in test_products:
        # 检查是否已存在
        if not Product.objects.filter(name=product_data['name']).exists():
            product = Product.objects.create(
                **product_data,
                created_by=admin_user
            )
            created_count += 1
            print(f"✓ 创建产品: {product.name} (库存: {product.quantity})")
    
    print(f"\n成功创建 {created_count} 个测试产品")
    print("=" * 60)
    
    # 显示统计信息
    stats = Product.objects.values('category').annotate(count=models.Count('id'), total_quantity=models.Sum('quantity'))
    print("\n库存统计：")
    print("-" * 40)
    for stat in stats:
        category_name = dict(Product.CATEGORY_CHOICES).get(stat['category'], stat['category'])
        print(f"{category_name}: {stat['count']}种产品，总计{stat['total_quantity'] or 0}件")
    
    total_products = Product.objects.count()
    total_quantity = Product.objects.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    print(f"\n总计: {total_products}种产品，{total_quantity}件库存")
    print("=" * 60)

if __name__ == '__main__':
    # 需要先导入 models 才能使用聚合函数
    from django.db import models
    create_test_products()