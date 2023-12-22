from django.db import models
from outpost.django.typo3.models import Category


class NewsCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )

    def __str__(self):
        return str(self.category)


class EventCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )

    def __str__(self):
        return str(self.category)
