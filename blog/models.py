from django.db import models

class Category(models.Model):
    """ 
    Категория публикаций. Один к многим публикаций
    """
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(verbose_name="Слаг", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"
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
            verbose_name = "Публикации"
            verbose_name_plural = "Публикации"
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


Post - модель (чертёж таблицы) - знает поля и связи, сами строки не трогает

post - объект (экземпляр) - одна строка из БД
- post.title, post.category.name - поля одной строки
- save() - сохраняет одну запись (создает новую или обновляет существующую)
- delete() - удаляет одну запись
- пока нет save() - база ничего не знает об изменениях


Post.objects - менеджер объектов: точка входа для операций над всей таблицей
Методы которые вернут объект Post
- get() - возвращает один объект Post; 0 строк - ошибка DoesNotExist, 2 и больше - MultipleObjectsReturned
- create() - создает новый объект Post и сразу сохраняет его в БД

Методы которые вернут кортеж (объект, флаг)
- get_or_create() - нашел по условиям или создал: (obj, True) - создал, (obj, False) - нашел
- update_or_create() - нашел и перезаписал поля из defaults или создал

Методы которые вернут QuerySet (набор-запрос: 0, 1 или много строк)
- all() - возвращает все записи
- filter(...) - записи которые подходят под фильтр (точное совпадение)
- exclude(...) - записи которые не подходят под фильтр
- order_by(...) - записи по полю, "-поле" - по убыванию
- values() - набор словарей, а не объектов Post
- values_list() - набор кортежей, а не объектов Post
- distinct() - записи без повторов
- annotate() - записи с добавленными значениями
- QuerySet склеивается в цепочки: filter(...).exclude(...).order_by("-id")
- он ленивый - запрос уходит в базу когда нужен результат (print, len, цикл)

Методы которые вернут объект Post или None
- first() - первый объект набора
- last() - последний объект набора

Методы которые вернут число
- count() - сколько записей
- update(...) - сколько записей изменили (массовый UPDATE)

Методы которые вернут True/False
- exists() - есть ли хоть одна запись

Методы которые вернут кортеж (всего, {модель: сколько})
- delete() - массовое удаление записей

Остальные
- bulk_create([...]) - список созданных объектов одной вставкой
- aggregate() - словарь с агрегатным значением

ЗАПРОСЫ УРОКА 55

python manage.py shell_plus --print-sql

1. .get Добыча по ключу Даст 1 Пост (не сет) или упадет если ИХ НЕТ или ИХ НЕСКОЛЬКО
post_1 = Post.objects.get(id=1)
post_1.category.name

post_666 = Post.objects.get(id=666) # blog.models.Post.DoesNotExist
post_2 = Post.objects.get(pk=2) # pk - primary key, т.е. id

2. create Создание нового поста - возвращает объект Post
category_adventures = Category.objects.get(slug="adventure")
new_post = Post.objects.create(title="Пост 3", text="Текст поста 3", category=category_adventures)

3. first и last дадут объект Post или None (первый или последний в наборе)
first_post = Post.objects.first()
last_post = Post.objects.last()
first_post
last_post

4. Проверка существования записи 
Post.objects.exists() - есть ли хоть одна запись в таблице Post
Post.objects.filter(id=1).exists() - есть ли запись с id=1
Post.objects.filter(title="чебурек").exists() - есть ли запись с title="чебурек"

5. Count - сколько записей в таблице Post
Post.objects.count() - сколько всего постов
Post.objects.filter(title="Пост 1").count() - сколько постов с title="Пост 1"

================= Методы которые дает queryset (набор-запрос) =================

5. all() - вернет все записи в виде QuerySet (набор-запрос)
all_posts = Post.objects.all()
all_posts - ВОТ ТУТ уже будет запрос в БД

6. filter(...) - вернет записи которые подходят под фильтр (точное совпадение)
filtered_posts = Post.objects.filter(title="Пост 1")
filtered_posts - ВОТ ТУТ уже будет запрос в БД

7. Получить все посты. Отфильтровать. Обратиться к переменной (тут будет уже запрос в БД)
all_posts = Post.objects.all()
filtered_posts = all_posts.filter(title="Пост 1")
filtered_posts - ВОТ ТУТ уже будет запрос в БД

8. Сортируем посты по убыванию title
sorted_posts = Post.objects.order_by("-id")
sorted_posts - ВОТ ТУТ уже будет запрос в БД

9. Можно ли все вместе?
some_posts = Post.objects.all().filter(title="Пост 1").order_by("-id")

some_posts[0].category.name

10. Добыча постов по названию категории category__name
posts_with_category_name = Post.objects.filter(category__name="Приключения")

11. Exclude - исключить записи которые подходят под фильтр (точное совпадение)
posts_without_category_name = Post.objects.exclude(category__name="Приключения")
"""