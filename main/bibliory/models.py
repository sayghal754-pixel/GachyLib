from django.db import models


class Book(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Краткое описание', blank=True)
    cover = models.ImageField('Обложка', upload_to='book_covers/', blank=True)
    file = models.FileField('Файл книги', upload_to='books/', blank=True)
    created_at = models.DateTimeField('Добавлена', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    def __str__(self):
        return self.title
