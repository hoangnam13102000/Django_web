from django.db import models

# Create your models here.

# Table Category
class Category(models.Model):
    name=models.CharField(max_length=255, db_index=True)
    class Meta:
        db_table='Category'
    def __str__(self):
        return self.name
    
# Table Product
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=500 )
    image=models.ImageField(upload_to='images',null=False, default=None)
    price=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    brand=models.CharField(max_length=255,null=False, default=None)
    class Meta:
        db_table='Product'
    def __str__(self):
        return self.title
# class Comment(models.Model):
#     product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
#     commenter_name = models.CharField(max_length=200)
#     comment_body = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)