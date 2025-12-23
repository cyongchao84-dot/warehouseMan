from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'quantity', 'price', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '产品名称',
            'description': '产品描述',
            'category': '产品类别',
            'quantity': '库存数量',
            'price': '单价',
            'location': '存放位置',
        }

class ProductSearchForm(forms.Form):
    """搜索表单"""
    name = forms.CharField(
        label='产品名称',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '输入产品名称...'
        })
    )
    category = forms.ChoiceField(
        label='类别',
        required=False,
        choices=[('', '所有类别')] + Product.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_quantity = forms.IntegerField(
        label='最小库存',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': '最小数量'
        })
    )