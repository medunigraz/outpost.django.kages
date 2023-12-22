import json

from braces.views import JSONResponseMixin
from django.urls import reverse
from django.utils import timezone
from django.views import View
from outpost.django.typo3.models import (
    Event,
    News,
)

from . import models
from .conf import settings


def create_news(news):
    media = news.media.filter(preview=True)
    if media.exists():
        image_url = media.first().media.url
    else:
        image_url = None
    return {
        "__metadata": {
            "uri": reverse("kages:transfer"),
            "etag": f'W/"{news.pk}"',
            "type": "Microsoft.SharePoint.DataService.NewsItem",
        },
        "InhaltstypID": settings.KAGES_NEWS_CONTENTTYPE_ID,
        "Titel": news.title,
        "StartDate": "/Date({d})/".format(d=int(news.start.timestamp() * 1000))
        if news.start
        else None,
        "EndDate": "/Date({d})/".format(d=int(news.end.timestamp() * 1000))
        if news.end
        else None,
        "ShortDescription": news.teaser,
        "ShowInArchive": True,
        "Link": news.url(),
        "ImageUrl": image_url,
        "KgJSON": json.dumps(
            {
                "Aktualisierungsdatum": news.last_modified.isoformat(),
                "Template": "meduni_news",
                "data": {
                    "Beitragsdatum": news.datetime.isoformat(),
                    "GeplantesEndedatum": news.end.isoformat() if news.end else None,
                    "GeplantesStartdatum": news.start.isoformat()
                    if news.start
                    else None,
                    "Inhaltstyp": "Med Uni News",
                    "Optionen": None,
                    "Redaktionen": None,
                    "TeaserBild": image_url,
                    "TeaserText": news.teaser,
                    "Text": news.body,
                    "Themen": [c.title for c in news.categories.all()],
                    "Titel": news.title,
                    "URL": news.url(),
                },
            }
        ),
        "Description": news.description,
        "MedOnlineId": news.pk,
        "NewsCategory": ", ".join([c.title for c in news.categories.all()]),
        "LastModified": "/Date({d})/".format(
            d=int(news.last_modified.timestamp() * 1000)
        )
        if news.end
        else None,
        "IsSpecial": news.topnews,
        "Published": True,
        "ID": news.pk,
        "Inhaltstyp": "News",
        "Geändert": "/Date({d})/".format(d=int(news.datetime.timestamp() * 1000))
        if news.datetime
        else None,
        "Erstellt": "/Date({d})/".format(d=int(news.datetime.timestamp() * 1000))
        if news.datetime
        else None,
        "ErstelltVon": news.author,
        "GeändertVon": news.author,
        "Pfad": "/Lists/News",
    }


def create_event(event):
    return


class TransferView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        entries = list()
        ncat = [n.category for n in models.NewsCategory.objects.all()]
        import pudb

        pu.db
        for news in News.objects.filter(
            categories__in=ncat,
            datetime__gt=timezone.now() - settings.KAGES_NEWS_LOOKBACK,
        ):
            entries.append(create_news(news))
        #        ecat = [e.category for e in models.EventCategory.objects.all()]
        #        for event in Event.objects.filter(category=ecat, end__gt=timezone.now()):
        #            entries.append(create_event(event))

        return self.render_json_response({"d": {"results": entries}})
