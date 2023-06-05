from django.db.models.signals import pre_save
from django.dispatch import receiver

from network.models import TradeUnit


@receiver(pre_save, sender=TradeUnit)
def set_tradeunit_level(sender, instance, **kwargs):
    if instance.unit_type == TradeUnit.UnitType.manufacture:
        if instance.provider:
            raise ValueError('Manufacture should not have provider')
        instance.level = 0
    elif instance.provider.unit_type == TradeUnit.UnitType.manufacture:
        instance.level = 1
    else:
        instance.level = instance.provider.level + 1
