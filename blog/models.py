from django.db import models

NULLABLE = {"blank": True, "null": True}


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.CharField(max_length=100, **NULLABLE, verbose_name="Slug")
    description = models.TextField(**NULLABLE, verbose_name="Содержимое")
    image = models.ImageField(upload_to="product/", **NULLABLE, verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="просмотров")
    author = models.ForeignKey(
        "main.Doctor",
        on_delete=models.CASCADE,
        verbose_name="автор",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.title}, {self.slug}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
