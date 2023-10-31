from django.shortcuts import render,redirect #Import render để render giao diện, redirect để chuyển hướng
from django.http import HttpResponse,JsonResponse #Import HttpResponse và JsonResponse để trả về response
from .models import * #Import tất cả các models từ app hiện tại
import json #Import json để encode/decode json
from django.contrib.auth.forms import UserCreationForm #Import form đăng ký user
from django.contrib.auth import authenticate,login,logout #Xác thực và đăng nhập/đăng xuất user
from django.contrib import messages #Để hiển thị các thông báo
from django.core.mail import send_mail #Gửi email 
from django.http import JsonResponse #Trả về JsonResponse
from .forms import ShippingAddressForm #Import form nhập địa chỉ giao hàng
from django.core.paginator import Paginator #Phân trang

# Create your views here.
def thankyou(request):
  return render(request, 'app/thankyou.html')

def purchase_history(request): #Lịch sử mua hàng của khách
    if request.user.is_authenticated: #Kiểm tra xem user đã đăng nhập chưa
        customer = request.user #Gán biến customer là user hiện tại
        orders = Order.objects.filter(customer=customer, complete=True).prefetch_related('orderitem_set__product')  
        #Lấy các đơn hàng có customer là user hiện tại và complete=True
        #Sử dụng prefetch_related để lấy kèm các order item và product cho performant
    else:#Nếu chưa đăng nhập
        orders = []   #Không có đơn hàng nào
    context = {'orders': orders}
    return render(request, 'app/purchase_history.html', context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        categories = Category.objects.filter(is_sub = False)
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    id = request.GET.get('id','')
    products = Product.objects.filter(id = id)
    categories = Category.objects.filter(is_sub = False)
    context = {'products':products,'items':items, 'order':order,'cartItems':cartItems,'categories':categories}
    return render(request, 'app/detail.html',context)

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {'categories':categories,'products':products,'active_category':active_category}
    return render(request, 'app/category.html',context)

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        keys = Product.objects.filter(name__icontains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        categories = Category.objects.filter(is_sub = False)
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        messages.error(request, 'Vui long dang nhap!')
        categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    return render(request, 'app/search.html',{'keys':keys,'searched':searched ,'products':products,'cartItems':cartItems,'categories':categories})
    
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():#Kiểm tra xem form có hợp lệ hay không
            form.save()#Nếu hợp lệ, lưu dữ liệu vào db
            return redirect('login')
    context = {'form':form}
    return render(request, 'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')  
            return redirect('home') 
        else:
            messages.info(request, 'Sai tài khoản hoặc mật khẩu')
    context = {}
    return render(request, 'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    # Lấy danh sách sản phẩm (tất cả sản phẩm)
    products = Product.objects.all()
    # Lấy 3 sản phẩm nổi bật
    first_three_products = products[:3]
    # Số lượng sản phẩm trên mỗi trang
    items_per_page = 8
    # Tạo một đối tượng Paginator để phân trang
    paginator = Paginator(products, items_per_page)
    # Lấy số trang từ tham số truy vấn (nếu có)
    page_number = request.GET.get('page')
    # Lấy danh sách sản phẩm cho trang hiện tại
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:#Kiểm Tra Xác Thực Người Dùng
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        messages.error(request, 'Vui lòng đăng nhập để tiếp tục mua sắm!')
    #lấy danh sách danh mục sản phẩm (Category) mà không phải là danh mục con (is_sub=False).
    categories = Category.objects.filter(is_sub=False)
    context = {
        'first_three_products': first_three_products,
        'page': page,
        'cartItems': cartItems,
        'categories': categories,
    }
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        categories = Category.objects.filter(is_sub = False)
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        categories = Category.objects.filter(is_sub = False)
    context = {'items':items, 'order':order,'cartItems':cartItems,'categories':categories}
    return render(request, 'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        categories = Category.objects.filter(is_sub=False)

        if request.method == 'POST':
            shipping_address_form = ShippingAddressForm(request.POST)
            if shipping_address_form.is_valid():
                address = shipping_address_form.cleaned_data['address']
                city = shipping_address_form.cleaned_data['city']
                recipient_name = shipping_address_form.cleaned_data['recipient_name']
                mobile = shipping_address_form.cleaned_data['mobile']

                # Check số lượng sản phẩm 
                for item in items:
                    product = item.product
                    if item.quantity > product.quantity:
                        messages.error(request, f"Sản phẩm '{product.name}' có số lượng không đủ.")
                        return redirect('checkout')

                # Proceed with the order
                shipping_address = ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=address,
                    city=city,
                    recipient_name=recipient_name,
                    mobile=mobile
                )
                # Cập nhật số lượng Product
                for item in items:
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
                # Mark the order as complete
                order.complete = True
                order.save()
                # Tạo 1 order mới
                new_order = Order.objects.create(customer=customer, complete=False)
                return redirect('thankyou')
            else:
                print(shipping_address_form.errors)
                messages.error(request, 'Vui lòng kiểm tra thông tin giao hàng.')
        else:
            shipping_address_form = ShippingAddressForm()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        categories = Category.objects.filter(is_sub=False)
        messages.error(request, 'Vui lòng đăng nhập để tiếp tục mua sắm!')

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'categories': categories}
    context['shipping_address_form'] = shipping_address_form
    return render(request, 'app/checkout.html', context)

    
   
def updateItem(request):
 if request.method == 'POST':
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    #Xóa khỏi trang cart khi orderItem <= 0
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

# def send_order_email(request):
#     if request.method == 'POST':
#         try:
#             customer = request.user
#             order = Order.objects.filter(customer=customer, complete=False).first() #Lấy đơn hàng chưa complete đầu tiên
#             if order:
#                 order_id = order.id
              
#             subject = 'Xác nhận đơn hàng' #Tiêu đề email
#             message = 'Cảm ơn bạn đã tin tưởng và đặt hàng. Đơn hàng của bạn đã được nhận.'+request.user.first_name + ' ' + request.user.last_name
#             message += f'\nID Đơn hàng: {order_id - 1}'
#             from_email = 'tomanhminh113@gmail.com'  # Email của bạn
#             recipient_email = request.user.email  # Email người nhận
            
#             send_mail(subject, message, from_email,[recipient_email], fail_silently=False)

#             response_data = {'success': True, 'message': 'Email đã được gửi thành công.'}
#             return HttpResponse(json.dumps(response_data), content_type="application/json")
#         except Exception as e:
#             response_data = {'success': False, 'message': str(e)}
#             return HttpResponse(json.dumps(response_data), content_type="application/json")

#     response_data = {'success': False, 'message': 'Yêu cầu không hợp lệ.'}
#     return HttpResponse(json.dumps(response_data), content_type="application/json")