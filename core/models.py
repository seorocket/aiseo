from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Proxy(models.Model):
    CHOICE_PROXY_STATUS = (
        (0, 'valid'),
        (1, 'error'),
        (2, 'stop')
    )

    CHOICE_PROXY_PROTOCOL = (
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
        ('socks4', 'SOCKS4'),
        ('socks5', 'SOCKS5'),
    )

    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    protocol = models.CharField(default='http', max_length=10, choices=CHOICE_PROXY_PROTOCOL)
    status = models.IntegerField(default=0, choices=CHOICE_PROXY_STATUS)

    def __str__(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.ip_address}:{self.port}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


CHOICE_SEARCHQUERY_STATUS = (
    (0, 'added'),
    (1, 'done'),
    (2, 'inprogress'),
    (3, 'error')
)


class SearchQuery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    status = models.IntegerField(default=0, choices=CHOICE_SEARCHQUERY_STATUS)
    status_name = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.status_name = dict(CHOICE_SEARCHQUERY_STATUS).get(int(self.status))
        super(SearchQuery, self).save(*args, **kwargs)

    def __str__(self):
        return self.query


CHOICE_DOMAIN_STATUS = (
    (0, 'added'),
    (1, 'check files'),
    (2, 'inprogress'),
    (3, 'get images'),
    (4, 'checked'),
    (5, 'get files'),
    (6, 'timestamps'),
)


class Domain(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    pages = models.IntegerField(default=0)
    history = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(default=0, choices=CHOICE_DOMAIN_STATUS)

    snippet = models.CharField(max_length=255, null=True, blank=True)
    image = models.IntegerField(default=0)
    first_captured = models.IntegerField(default=0)
    stripped_snippet = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    thumb = models.CharField(max_length=255, null=True, blank=True)
    capture = models.IntegerField(default=0)
    video = models.IntegerField(default=0)
    webpage = models.IntegerField(default=0)
    audio = models.IntegerField(default=0)
    last_captured = models.IntegerField(default=0)
    status_name = models.CharField(max_length=50, blank=True, null=True)

    @property
    def files_count(self):
        return File.objects.filter(domain=self).count()

    def save(self, *args, **kwargs):
        self.status_name = dict(CHOICE_DOMAIN_STATUS).get(int(self.status))
        super(Domain, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DomainImages(models.Model):
    class Meta:
        verbose_name = u"Domain Image"
        verbose_name_plural = u"Domain Images"

    photo = models.FileField('Image', upload_to='image_domain', null=True, blank=True)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE, default=1, related_name='images_domain')


CHOICE_FILE_STATUS = (
    (3, 'Done'),
    (2, 'Inprogress'),
    (1, 'ToDo'),
    (0, 'Error'),
)


class File(models.Model):
    url = models.CharField(max_length=1255000, unique=True)
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.CharField(max_length=20, null=True, blank=True)
    endtimestamp = models.CharField(max_length=20, null=True, blank=True)
    shots = models.TextField(null=True, blank=True)
    groupcount = models.IntegerField(null=True, blank=True)
    uniqcount = models.IntegerField(null=True, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHOICE_FILE_STATUS, default=1)
    content = models.TextField(max_length=314572800, null=True, blank=True)

    # Добавляем поле для загрузки файла
    file = models.FileField(upload_to='', null=True, blank=True)  # '/' - это путь для сохранения файлов на сервере

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"


CHOICE_SHOT_STATUS = (
    (3, 'Done'),
    (2, 'Inprogress'),
    (1, 'ToDo'),
    (0, 'Error'),
)


class Shot(models.Model):
    name = models.CharField(max_length=99999, verbose_name=u"Shot")
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateField(default='1000-01-01')
    status = models.IntegerField(default=1,choices=CHOICE_SHOT_STATUS)
    timestamp = models.IntegerField()
    statuscode = models.IntegerField()
    digest = models.CharField(max_length=30)
    length = models.IntegerField()

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