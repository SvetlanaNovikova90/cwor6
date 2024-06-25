from django.db import models


class Blog(models.Model):
    """
    Модель для создания блоговой записи
    """
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(upload_to='media/', verbose_name='изображение')
    create_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0, verbose_name='кол-во просмотров')
    date = models.DateTimeField(auto_now=True, editable=False, verbose_name='дата создания')

    def __str__(self):
        return f'{self.title}. {self.content}.'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блог'
        ordering = ('title',)
