# Generated for the initial library model.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('cover', models.ImageField(blank=True, upload_to='book_covers/', verbose_name='Обложка')),
                ('file', models.FileField(blank=True, upload_to='books/', verbose_name='Файл книги')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлена')),
            ],
            options={
                'verbose_name': 'книга',
                'verbose_name_plural': 'книги',
                'ordering': ('-created_at',),
            },
        ),
    ]
