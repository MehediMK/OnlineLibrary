from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
# import datetime
from datetime import datetime, timedelta

# Create your models here.

class User_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    GENDER_CHOICE= (('M','Male'),('F','Female'),('OG','Other'))
    profile_pic = models.ImageField(upload_to='profilepic',blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE,blank=True)
    address = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return "User: {},Genger: {}".format(self.user.first_name, self.gender)


class Book_category(models.Model):
    name = models.CharField(max_length=100,blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100,blank=False)
    category = models.ForeignKey(Book_category,on_delete=models.CASCADE)
    author = models.CharField(max_length=100,blank=False)
    page_no = models.IntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    book_photo = models.ImageField(upload_to='booksphoto')
    book_pdf = models.FileField(upload_to='bookpdf')
    description = models.TextField(max_length=1600)
    upload_date = models.DateTimeField(auto_now_add=True)

    def short_desc(self):
        return self.description[:50]
    
    @staticmethod
    def get_books_by_id(ides):
        return Book.objects.filter(id__in=ides)


    def __str__(self):
        return "Book Name:{}, Category:{}".format(self.book_name, self.category)


class Book_package(models.Model):
    pack_name = models.CharField(max_length=100)
    max_book = models.IntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pack_name


class Online_read_pack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book_pack = models.ForeignKey(Book_package,on_delete=models.CASCADE)
    payment_traxid = models.CharField(max_length=200, blank=False)
    issu_date = models.DateTimeField(auto_now=True,blank=False)
    end_date = models.DateTimeField(editable=False)

    @staticmethod
    def get_orders_by_user(myuser):
        # return Online_read_pack.objects.filter(user=myuser).exists()

        return Online_read_pack.objects.filter(Q(user=myuser), Q(end_date__gte = datetime.now())).exists()


    def save(self):
        # from datetime import datetime, timedelta
        d = timedelta(days=30)

        if not self.id:
            self.end_date = datetime.now() + d
            super(Online_read_pack, self).save()

    def __str__(self):
        return "User: {} ,Book List: {}".format(self.user.username,self.book_pack.pack_name)

class Online_read_book_list(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book_list = models.ForeignKey(Book,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


    @staticmethod
    def get_orders_by_Id(id):
        return Online_read_book_list.objects.filter(book_list__id=id).exists()
        

    def __str__(self):
        return "User: {} , Book_name: {}".format(self.user.username,self.book_list.book_name)

    
class Order(models.Model):
    product = models.ForeignKey(Book,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    bkashTrxID = models.CharField(max_length=150,default='',blank=True)
    address = models.CharField(max_length=150,default='')
    phone = models.CharField(max_length=15,default='')
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-id')

