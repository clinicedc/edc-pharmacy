from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class Medication (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "edc_pharma"
