from django.contrib import admin
from .models import Book_category,Book,Book_package,User_info,Online_read_pack,Online_read_book_list,Order

# Register your models here.
admin.site.register(User_info)
admin.site.register(Book_category)
admin.site.register(Book)
admin.site.register(Book_package)
admin.site.register(Online_read_book_list)
admin.site.register(Online_read_pack)
admin.site.register(Order)
