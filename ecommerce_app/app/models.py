from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
  ('CR', 'Curd'),
  ('ML', 'Milk'),
  ('LS', 'Lassi'),
  ('MS', 'Milkshake'),
  ('PN', 'Paneer'),
  ('GH', 'Ghee'),
  ('CZ', 'chess'),
  ('IC', 'Ice-Creams'),
)
class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()
  composition = models.TextField()
  prodapp = models.TextField()
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  product_image = models.ImageField(upload_to='product')
  def _str_(self):
    return self.title