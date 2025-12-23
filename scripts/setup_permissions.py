import os
import sys
import django

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warehouse_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from warehouse.models import Product

def setup_permissions():
    """设置用户权限"""
    print("=" * 60)
    print("开始设置用户权限")
    print("=" * 60)
    
    # 1. 确保权限存在
    content_type = ContentType.objects.get_for_model(Product)
    
    permissions_data = [
        ('can_view_product', '可以查看产品'),
        ('can_add_product', '可以添加产品'),
        ('can_change_product', '可以修改产品'),
        ('can_delete_product', '可以删除产品'),
        ('can_search_product', '可以搜索产品'),
    ]
    
    for codename, name in permissions_data:
        Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type
        )
        print(f"✓ 权限已创建: {name}")
    
    # 2. 创建用户组
    groups = {
        '仓库管理员': [
            'can_view_product',
            'can_add_product', 
            'can_change_product',
            'can_delete_product',
            'can_search_product',
        ],
        '仓库查看员': [
            'can_view_product',
            'can_search_product',
        ],
        '仓库操作员': [
            'can_view_product',
            'can_add_product',
            'can_change_product',
            'can_search_product',
        ],
    }
    
    for group_name, perms in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for codename in perms:
            try:
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"✗ 权限不存在: {codename}")
        
        if created:
            print(f"✓ 创建组: {group_name}")
        else:
            print(f"↻ 组已存在: {group_name}")
    
    # 3. 创建测试用户
    users = [
        ('admin', 'admin@example.com', 'admin123', ['仓库管理员'], True, True),
        ('manager', 'manager@example.com', 'manager123', ['仓库管理员'], False, True),
        ('viewer', 'viewer@example.com', 'viewer123', ['仓库查看员'], False, True),
        ('operator', 'operator@example.com', 'operator123', ['仓库操作员'], False, True),
        ('test_user', 'test@example.com', 'test123', [], False, False),
    ]
    
    for username, email, password, group_names, is_superuser, is_staff in users:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_superuser': is_superuser, 'is_staff': is_staff}
        )
        
        if created:
            user.set_password(password)
            user.save()
            
            # 分配组
            for group_name in group_names:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            
            print(f"✓ 创建用户: {username} ({password})")
        else:
            print(f"↻ 用户已存在: {username}")
    
    print("\n" + "=" * 60)
    print("权限设置完成！")
    print("=" * 60)
    print("\n测试账户信息：")
    print("-" * 30)
    for username, _, password, group_names, _, _ in users[:4]:
        groups_str = ', '.join(group_names) if group_names else '无权限'
        print(f"用户名: {username}")
        print(f"密码: {password}")
        print(f"权限组: {groups_str}")
        print("-" * 30)

if __name__ == '__main__':
    setup_permissions()