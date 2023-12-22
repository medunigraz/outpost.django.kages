from appconf import AppConf
from django.conf import settings
from django.utils import timezone


class BaseAppConf(AppConf):
    PERS_ID_FILTER = "(CO-KAGESPERSNR-N={id})"
    PERS_FIELDS = [
        "cn",
        "mail",
        "givenName",
        "sn",
        "CO-ACCOUNTTYPE-C",
        "CO-PERSNRSSO-C",
    ]
    NEWS_CONTENTTYPE_ID = (
        "0x0100EBBF53831DBD49D3B3D054F93BADCC8100FDF8B9EBFA0A7E4ABB1AA86B2B27687E"
    )
    NEWS_LOOKBACK = timezone.timedelta(days=30)

    class Meta:
        prefix = "kages"
