from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES =(
    ('An Giang', 'An Giang'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cần Thơ', 'Cần Thơ'),  # City
    ('Cao Bằng', 'Cao Bằng'),
    ('Đà Nẵng', 'Đà Nẵng'),  # City
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Nội', 'Hà Nội'),  # City
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),  # City
    ('Hậu Giang', 'Hậu Giang'),
    ('Hồ Chí Minh', 'Hồ Chí Minh'),  # City
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
)
CATEGORY_CHOICES = (
  ('CR', 'Curd'),
  ('ML', 'Milk'),
  ('LS', 'Lassi'),
  ('MS', 'Milkshake'),
  ('PN', 'Paneer'),
  ('GH', 'Ghee'),
  ('CZ', 'Cheese'),
  ('IC', 'Ice-Creams'),
)

class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()
  composition = models.TextField(default="")
  prodapp = models.TextField(default="")
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  product_image = models.ImageField(upload_to='product')

  def __str__(self):
    return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),       # Đã chấp nhận
    ('Packed', 'Packed'),           # Đã đóng gói
    ('On The Way', 'On The Way'),   # Đang trên đường giao
    ('Delivered', 'Delivered'),     # Đã giao hàng
    ('Cancel', 'Cancel'),           # Đã hủy
    ('Pending', 'Pending'),         # Đang chờ xử lý
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
