from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm, ProductSearchForm

@login_required
@permission_required('warehouse.can_view_product', raise_exception=True)
def product_list(request):
    """产品列表视图"""
    products = Product.objects.all()
    search_form = ProductSearchForm(request.GET or None)
    
    if search_form.is_valid() and request.user.has_perm('warehouse.can_search_product'):
        name = search_form.cleaned_data.get('name')
        category = search_form.cleaned_data.get('category')
        min_quantity = search_form.cleaned_data.get('min_quantity')
        
        if name:
            products = products.filter(name__icontains=name)
        if category:
            products = products.filter(category=category)
        if min_quantity is not None:
            products = products.filter(quantity__gte=min_quantity)
    
    context = {
        'products': products,
        'search_form': search_form,
        'can_add': request.user.has_perm('warehouse.can_add_product'),
        'can_search': request.user.has_perm('warehouse.can_search_product'),
    }
    return render(request, 'warehouse/product_list.html', context)

@login_required
@permission_required('warehouse.can_view_product', raise_exception=True)
def product_detail(request, pk):
    """产品详情视图"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'can_change': request.user.has_perm('warehouse.can_change_product'),
        'can_delete': request.user.has_perm('warehouse.can_delete_product'),
    }
    return render(request, 'warehouse/product_detail.html', context)

@login_required
@permission_required('warehouse.can_add_product', raise_exception=True)
def product_create(request):
    """创建产品视图"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, '产品创建成功！')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'warehouse/product_form.html', {
        'form': form,
        'title': '创建新产品'
    })

@login_required
@permission_required('warehouse.can_change_product', raise_exception=True)
def product_update(request, pk):
    """更新产品视图"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '产品更新成功！')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'warehouse/product_form.html', {
        'form': form,
        'title': f'编辑产品: {product.name}',
        'product': product,
    })

@login_required
@permission_required('warehouse.can_delete_product', raise_exception=True)
def product_delete(request, pk):
    """删除产品视图"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, '产品删除成功！')
        return redirect('product_list')
    
    return render(request, 'warehouse/product_confirm_delete.html', {
        'product': product
    })
    from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')