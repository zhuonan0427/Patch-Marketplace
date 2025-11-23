# marketplace/forms.py
from django import forms
from goods.models import Goods, GoodsImage, OutcomeImage


class GoodsForm(forms.ModelForm):
    """商品发布/编辑表单"""

    class Meta:
        model = Goods
        fields = [
            'name', 'price', 'description',
            'major', 'professor', 'category', 'course_code',
            'amount_usage', 'payment_methods', 'additional_info',
            'outcome_description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'e.g., Watercolor Paint Set'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'Describe your item...',
                'rows': 4
            }),
            'major': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg'
            }),
            'professor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'e.g., S. Maku'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'e.g., DSD-3003-B'
            }),
            'amount_usage': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'How much is left? How used is it?',
                'rows': 3
            }),
            'payment_methods': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'e.g., Venmo, Cash, Apple Pay'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'Any other details...',
                'rows': 3
            }),
            'outcome_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border rounded-lg',
                'placeholder': 'Describe the artworks created with this item...',
                'rows': 3
            }),
        }
        labels = {
            'name': 'Item Name',
            'price': 'Price ($)',
            'description': 'Description',
            'major': 'Major',
            'professor': 'Professor',
            'category': 'Category',
            'course_code': 'Course Code',
            'amount_usage': 'Amount & Usage',
            'payment_methods': 'Accepted Payment Methods',
            'additional_info': 'Additional Information',
            'outcome_description': 'Outcome Description',
        }


class GoodsImageForm(forms.ModelForm):
    """商品图片表单"""

    class Meta:
        model = GoodsImage
        fields = ['image', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-20 px-2 py-1 border rounded',
                'min': '0'
            })
        }


class OutcomeImageForm(forms.ModelForm):
    """Outcome图片表单"""

    class Meta:
        model = OutcomeImage
        fields = ['image', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-20 px-2 py-1 border rounded',
                'min': '0'
            })
        }