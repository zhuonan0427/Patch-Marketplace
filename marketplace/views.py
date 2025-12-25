# marketplace/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db import models
from goods.models import Goods, Message, Favorite, GoodsImage, OutcomeImage
import random


def home(request):
    """首页视图"""
    return render(request, 'marketplace/home.html')


# 在 marketplace/views.py 的 shop 函数中修改

def shop(request):
    """商品列表页视图 + 搜索筛选"""
    items = Goods.objects.all()

    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(professor__icontains=search_query) |
            models.Q(course_code__icontains=search_query)
        )

    # 筛选功能
    major_filter = request.GET.get('major', '')
    category_filter = request.GET.get('category', '')

    if major_filter:
        items = items.filter(major=major_filter)
    if category_filter:
        items = items.filter(category=category_filter)

    # 获取所有可能的筛选选项
    majors = Goods.MAJOR_CHOICES
    categories = Goods.CATEGORY_CHOICES

    # 获取选中筛选的显示名称
    selected_title = "All"
    if major_filter:
        selected_title = dict(majors).get(major_filter, "All")
    elif category_filter:
        selected_title = dict(categories).get(category_filter, "All")
    elif search_query:
        selected_title = f'Search: "{search_query}"'

    context = {
        'items': items,
        'search_query': search_query,
        'major_filter': major_filter,
        'category_filter': category_filter,
        'majors': majors,
        'categories': categories,
        'selected_title': selected_title,  # 新增
    }
    return render(request, 'marketplace/shop.html', context)


def item_detail(request, item_id):
    """商品详情页"""
    item = get_object_or_404(Goods, id=item_id)

    # 获取相关商品 (同一category或major)
    related_items = Goods.objects.filter(
        models.Q(category=item.category) | models.Q(major=item.major)
    ).exclude(id=item.id)[:4]

    # 检查当前用户是否收藏
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, item=item).exists()

    context = {
        'item': item,
        'related_items': related_items,
        'is_favorited': is_favorited
    }
    return render(request, 'marketplace/item_detail.html', context)


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Patch!, {user.username}!')
            return redirect('marketplace:home')
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})


def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('marketplace:shop')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/login.html', {'form': form})


def user_logout(request):
    """用户登出"""
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('marketplace:home')


@login_required
def my_account(request):
    """我的账户"""
    my_items = Goods.objects.filter(seller=request.user) if hasattr(Goods, 'seller') else []
    context = {'my_items': my_items}
    return render(request, 'marketplace/my_account.html', context)


@login_required
def post_item(request):
    """发布商品"""
    from marketplace.forms import GoodsForm

    if request.method == 'POST':
        form = GoodsForm(request.POST)
        images = request.FILES.getlist('product_images')
        outcome_images = request.FILES.getlist('outcome_images')

        if form.is_valid():
            item = form.save(commit=False)
            # 如果Goods模型有seller字段,关联当前用户
            if hasattr(item, 'seller'):
                item.seller = request.user
            item.save()

            # 保存商品图片
            for i, img in enumerate(images[:3]):  # 最多3张
                GoodsImage.objects.create(goods=item, image=img, order=i)

            # 保存Outcome图片
            for i, img in enumerate(outcome_images[:5]):  # 最多5张
                OutcomeImage.objects.create(goods=item, image=img, order=i)

            messages.success(request, 'Item posted successfully!')
            return redirect('marketplace:my_account')
    else:
        form = GoodsForm()

    return render(request, 'marketplace/post_item.html', {'form': form})


@login_required
def edit_item(request, item_id):
    """编辑商品"""
    from marketplace.forms import GoodsForm
    item = get_object_or_404(Goods, id=item_id)

    # 检查权限(如果有seller字段)
    if hasattr(item, 'seller') and item.seller != request.user:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('marketplace:shop')

    if request.method == 'POST':
        form = GoodsForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('marketplace:my_account')
    else:
        form = GoodsForm(instance=item)

    return render(request, 'marketplace/edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, item_id):
    """删除商品"""
    item = get_object_or_404(Goods, id=item_id)

    # 检查权限
    if hasattr(item, 'seller') and item.seller != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('marketplace:shop')

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('marketplace:my_account')

    return render(request, 'marketplace/delete_confirm.html', {'item': item})


@login_required
def message_seller(request, item_id):
    """给卖家留言"""
    item = get_object_or_404(Goods, id=item_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                item=item,
                sender=request.user,
                content=content
            )
            messages.success(request, 'Message sent!')
            return redirect('marketplace:message_seller', item_id=item.id)

    # 获取该商品的所有留言
    item_messages = Message.objects.filter(item=item).select_related('sender')

    context = {
        'item': item,
        'item_messages': item_messages
    }
    return render(request, 'marketplace/message_seller.html', context)


@login_required
def toggle_favorite(request, item_id):
    """收藏/取消收藏"""
    item = get_object_or_404(Goods, id=item_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

    if not created:
        # 已存在,则删除(取消收藏)
        favorite.delete()
        messages.success(request, 'Removed from favorites')
    else:
        # 新创建(添加收藏)
        messages.success(request, 'Added to favorites!')

    return redirect('marketplace:item_detail', item_id=item.id)


@login_required
def favorites_list(request):
    """我的收藏列表"""
    favorites = Favorite.objects.filter(user=request.user).select_related('item')

    context = {'favorites': favorites}
    return render(request, 'marketplace/favorites.html', context)


@login_required
def checkout(request, item_id):
    """支付页面"""
    item = get_object_or_404(Goods, id=item_id)

    if request.method == 'POST':
        # 获取表单数据
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        payment_method = request.POST.get('payment_method')
        pickup_location = request.POST.get('pickup_location')

        # 生成订单号（演示用）
        order_number = f"PATCH{random.randint(10000, 99999)}"

        # 重定向到确认页面，传递数据
        return render(request, 'marketplace/payment_complete.html', {
            'item': item,
            'payment_method': payment_method,
            'pickup_location': pickup_location,
            'order_number': order_number,
            'full_name': full_name,
            'email': email,
        })

    return render(request, 'marketplace/checkout.html', {
        'item': item,
    })