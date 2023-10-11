from django.db import models
from ckeditor.fields import RichTextField


class Proxy(models.Model):
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ip_address}:{self.port}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SearchQuery(models.Model):
    CHOICE_SEARCHQUERY_STATUS = (
        (0, 'added'),
        (1, 'done'),
        (2, 'inprogress')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    status = models.IntegerField(default=0, choices=CHOICE_SEARCHQUERY_STATUS)
    def __str__(self):
        return self.query


class Domain(models.Model):
    CHOICE_DOMAIN_STATUS = (
        (0, 'added'),
        (1, 'check files'),
        (2, 'inprogress')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    pages = models.IntegerField(default=0)
    history = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(default=0, choices=CHOICE_DOMAIN_STATUS)
    def __str__(self):
        return self.name


class File(models.Model):
    CHOICE_FILE_STATUS = (
        (3, 'Done'),
        (2, 'Inprogress'),
        (1, 'ToDo'),
        (0, 'Error'),
    )
    url = models.CharField(max_length=1255, unique=True)
    mimetype = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=20)
    endtimestamp = models.CharField(max_length=20)
    shots = models.TextField(null=True, blank=True)
    groupcount = models.IntegerField()
    uniqcount = models.IntegerField()
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHOICE_FILE_STATUS, default=1)
    content = models.TextField(max_length=314572800, null=True, blank=True)

    # Добавляем поле для загрузки файла
    file = models.FileField(upload_to='')  # '/' - это путь для сохранения файлов на сервере

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"

class Shot(models.Model):
    CHOICE_SHOT_STATUS = (
        (3, 'Done'),
        (2, 'Inprogress'),
        (1, 'ToDo'),
        (0, 'Error'),
    )
    name = models.CharField(max_length=99999, verbose_name=u"ID")
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateField(default='1000-01-01')
    status = models.IntegerField(default=1,choices=CHOICE_SHOT_STATUS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Snapshot"
        verbose_name_plural = u"Snapshot's"


class Page(models.Model):
    class Meta:
        abstract = True

    alias = models.SlugField(max_length=200, verbose_name=u"Url", null=True)
    seo_h1 = models.CharField(max_length=200, verbose_name="H1", null=True, blank=True)
    seo_title = models.CharField(max_length=200, verbose_name="Title", null=True, blank=True)
    seo_description = models.CharField(max_length=500, verbose_name="Description", null=True, blank=True)
    content = RichTextField(null=True, blank=True)


class TextPage(Page):
    class Meta:
        verbose_name = "page"
        verbose_name_plural = "Pages"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name