from django.db import models


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


class Domain(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SearchQuery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    impressions = models.FloatField()
    ctr = models.FloatField()
    clicks = models.FloatField()
    position = models.FloatField()
    demand = models.FloatField()
    def __str__(self):
        return self.query


