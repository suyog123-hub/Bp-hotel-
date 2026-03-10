from django.contrib import admin
from .models import MenuTitle,menu_items,gallery_img,review1
# Register your models here.
admin.site.register(MenuTitle)
@admin.register(menu_items)
class menu_itemsAdmin(admin.ModelAdmin):
    list_display=['id','category','title','desc','price']


admin.site.register(gallery_img)

@admin.register(review1)
class review1Admin(admin.ModelAdmin):
    list_display=['id','name','desc','short_desc']