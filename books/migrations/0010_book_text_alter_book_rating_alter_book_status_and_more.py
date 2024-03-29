# Generated by Django 4.1.2 on 2022-12-13 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_stripe_book_price_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='text',
            field=models.FileField(blank=True, default=None, null=True, upload_to='book_texts', verbose_name='Текст книги'),
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.CharField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0, max_length=1, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[(0, 'Читаю'), (1, 'Закончена'), (2, 'Буду читать'), (3, 'Заинтересовала'), (4, 'Заброшена')], default=1, max_length=1, verbose_name='Статус'),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
