from __future__ import unicode_literals

from django.db import models

from dj_cqrs.constants import ALL_BASIC_FIELDS
from dj_cqrs.mixins import MasterMixin


class BasicFieldsModel(MasterMixin, models.Model):
    CQRS_ID = 'basic'

    int_field = models.IntegerField(primary_key=True)
    bool_field = models.NullBooleanField()
    char_field = models.CharField(max_length=200, null=True)
    date_field = models.DateField(null=True)
    datetime_field = models.DateTimeField(null=True)
    float_field = models.FloatField(null=True)
    url_field = models.URLField(null=True)
    uuid_field = models.UUIDField(null=True)


class AllFieldsModel(MasterMixin, models.Model):
    CQRS_FIELDS = ALL_BASIC_FIELDS
    CQRS_ID = 'all'

    int_field = models.IntegerField(null=True)
    char_field = models.CharField(max_length=200, null=True)


class ChosenFieldsModel(MasterMixin, models.Model):
    CQRS_FIELDS = ('char_field', 'id')
    CQRS_ID = 'chosen'

    float_field = models.IntegerField(null=True)
    char_field = models.CharField(max_length=200, null=True)


class AutoFieldsModel(MasterMixin, models.Model):
    CQRS_ID = 'auto'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class SimplestModel(MasterMixin, models.Model):
    CQRS_ID = 'pk'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)


class Publisher(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)


class Author(MasterMixin, models.Model):
    CQRS_ID = 'author'
    CQRS_SERIALIZER = 'tests.dj_master.serializers.AuthorSerializer'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    publisher = models.ForeignKey(
        Publisher, related_name='authors', on_delete=models.SET_NULL, null=True,
    )

    @classmethod
    def relate_cqrs_serialization(cls, queryset):
        return queryset.select_related('publisher').prefetch_related('books')


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)

    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)


class BadSerializationClassModel(MasterMixin, models.Model):
    CQRS_ID = 'bad_serialization'
    CQRS_SERIALIZER = 'tests.Serializer'
