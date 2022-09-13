from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """ Категории """
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Movie(models.Model):
    """ Фильмы """
    title = models.CharField("Название", max_length=150)
    tagline = models.CharField("Слоган", max_length=300, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Фото", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Год выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField("Persons", verbose_name="Режиссеры", related_name="film_director")
    actors = models.ManyToManyField("Persons", verbose_name="Актеры", related_name="film_actor")
    genres = models.ManyToManyField("Genres", verbose_name="Жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.CharField("Бюджет", max_length=20)
    world_profit = models.CharField("Сборы в мире", max_length=20)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.comment_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Frame(models.Model):
    """ Кадры из фильма """
    title = models.CharField("Заголовок", max_length=160)
    description = models.TextField("Описание")
    image = models.ImageField("Кадр", upload_to="frames/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class Persons(models.Model):
    """ Актеры\Режиссеры """
    name = models.CharField("Имя", max_length=150)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Stars(models.Model):
    """ Звезды рейтинга """
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звузды рейтинга"


class Rating(models.Model):
    """ Рейтинг """
    ip = models.CharField("IP адрес", max_length=16)
    star = models.ForeignKey(Stars, verbose_name="Звезда", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"


class Comment(models.Model):
    """ Отзывы """
    email = models.EmailField()
    name = models.CharField("Имя", max_length=50)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Genres(models.Model):
    """ Жанры """
    name = models.CharField("Жанр", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
