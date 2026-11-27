from django.db import models

class Category(models.Model):
    """ 
    Категория публикаций. Один к многим публикаций
    """
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(verbose_name="Слаг", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Публикации"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Публикация. Один ко многим котигориях
    """
    title = models.CharField(verbose_name="Заголовок", max_length=200)
    text = models.TextField(verbose_name="Текст")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="posts",
    )

    class Meta:
            verbose_name = "Категория"
            verbose_name_plural = "Категория"
            ordering = ["id"]
    
    def __str__(self):
        return self.title
    
"""
Создадим несколько категорий

Category.objects.create(name="Наука", slug="science")
Category.objects.create(name="Приключения", slug="adventures")
Category.objects.create(name="Семейные катастрофы", slug="family-disasters")

categories = Category.objects.all()
categories - получаю служебный QuerySet
categories[0] - получаю объект Category
categories[0].name - получаю название категории


# Добыть категорию с id=1
cat_1 = Category.objects.get(id=1) # Тут можно использовать pk=1
cat_1 - получаю экземпляр класса Category с данными из БД
cat_1.name - получаю название категории с id=1

# Обновить категорию с id=1
cat_1.name = "Увлекательная наука"
cat_1.save()
==============


Попробую создать пост с текстом и тайтлом без категории ОШИБКА
Post.objects.create(title="Пост 1", text="Текст поста 1")

# Категория по слагу adventures
cat_adventures = Category.objects.get(slug="adventure")

# Создать пост с категорией adventures
Post.objects.create(title="Пост 1", text="Текст поста 1", category=cat_adventures)

# Создаем пост 2
post_2 = Post.objects.create(title="Пост 2", text="Текст поста 2", category=cat_adventures)

проверим
post_2

post_2.category.name

posts_adv = cat_adventures.posts.all() - получаем все посты с категорией adventures
"""