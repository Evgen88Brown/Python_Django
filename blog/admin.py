from django.contrib import admin

from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug") # какие поля показывает в списке категорий
    search_fields = ("name", "slug") # какие поля будут участвовать в поиске по категории


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category") # какие поля показывает в списке публикаций
    search_fields = ("title", "text") # какие поля будут участвовать в поиске по публикациям
    list_filter = ("category",) # по каким полям пожно фильтровать публикации 

    