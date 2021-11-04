from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from edc_pharmacy.dispensing import Dispensing
from edc_pharmacy.models import RxRefill

from ..refill_creator import RefillCreator
from .dispensing_history import DispensingHistory


@receiver(
    post_save, sender=DispensingHistory, dispatch_uid="dispensing_history_on_post_save"
)
def dispensing_history_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        dispensing = Dispensing(
            rx_refill=instance.rx_refill, dispensed=instance.dispensed
        )
        instance.rx_refill.remaining = dispensing.remaining
        instance.rx_refill.save(update_fields=["remaining"])


@receiver(
    post_delete,
    sender=DispensingHistory,
    dispatch_uid="dispensing_history_on_post_delete",
)
def dispensing_history_on_post_delete(sender, instance, using=None, **kwargs):
    dispensing = Dispensing(rx_refill=instance.rx_refill, dispensed=instance.dispensed)
    instance.rx_refill.remaining = dispensing.remaining
    instance.rx_refill.save(update_fields=["remaining"])


@receiver(
    post_save,
    dispatch_uid="create_next_refill_on_post_save",
)
def create_next_refill_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        try:
            instance.creates_refills_from_crf
        except AttributeError:
            pass
        else:
            if not RxRefill.objects.filter(
                rx__subject_identifier=instance.subject_visit.subject_identifier
            ).exists():
                number_of_days = 0
                if instance.subject_visit.appointment.next:
                    number_of_days = (
                        instance.subject_visit.appointment.next.appt_datetime
                        - instance.subject_visit.appointment.appt_datetime
                    ).days
                RefillCreator(
                    subject_identifier=instance.subject_visit.subject_identifier,
                    refill_date=instance.subject_visit.appointment.appt_datetime,
                    number_of_days=number_of_days,
                    dosage_guideline=instance.next_dosage_guideline,
                    formulation=instance.next_formulation,
                    make_active=True,
                )
            if instance.subject_visit.appointment.next:
                number_of_days = 0
                if instance.subject_visit.appointment.next.next:
                    number_of_days = (
                        instance.subject_visit.appointment.next.next.appt_datetime
                        - instance.subject_visit.appointment.next.appt_datetime
                    ).days
                RefillCreator(
                    subject_identifier=instance.subject_visit.subject_identifier,
                    refill_date=instance.subject_visit.appointment.next.appt_datetime,
                    number_of_days=number_of_days,
                    dosage_guideline=instance.next_dosage_guideline,
                    formulation=instance.next_formulation,
                    make_active=False,
                )
