from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from main.slug import unique_slugify


class Ip(models.Model): # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class CategoryArticles(models.Model):
    title = models.CharField(max_length=255, blank=True, db_index=True)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    # формирование абсолютного url
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id', ]


class Articles(models.Model):
    title = models.CharField("Title", max_length=100)
    category = models.ForeignKey(CategoryArticles, verbose_name='Category', on_delete=models.SET_NULL, null=True)
    annotation = models.TextField("Annotation", blank=True)
    # content = models.TextField("Content", blank=True)
    content = RichTextUploadingField("Content", blank=True)
    image = models.ImageField("Image", upload_to="photos/posts/%Y/%m/%d")
    time_created = models.DateTimeField("Date created", auto_now_add=True)
    time_modified = models.DateTimeField("Date modified", auto_now=True)
    draft = models.BooleanField("Draft", default=False)
    slug = models.SlugField("URL", max_length=255, unique=True, db_index=True)
    # просмотры
    views = models.ManyToManyField(Ip, related_name="post_views", blank=True)

    # считаем количество просмотров
    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title

    # формирование абсолютного url
    def get_absolute_url(self):
        return reverse('article', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-id']

    def save(self, **kwargs):
        slug = '%s' % (self.title)
        unique_slugify(self, slug)
        super(Articles, self).save()
