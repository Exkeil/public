import factory

from bitrix_downloader.common.entities.bitrix import BitrixMassSelectionModel


class BitrixMassSelectionTableFactory(factory.Factory):
    class Meta:
        model = BitrixMassSelectionModel

    id = factory.Sequence(lambda n: n)
    stage = factory.Sequence(lambda n: f"stage_id_{n}")
    assessment_date = factory.Faker("date_time")
    solution = factory.Sequence(lambda n: n)
    user_name = factory.Sequence(lambda n: f"stage_id_{n}")
    comments = factory.Sequence(lambda n: n)
    sp = factory.Sequence(lambda n: n)
    body_check = factory.Sequence(lambda n: n)
    age = factory.Sequence(lambda n: n)
    employment_stage = factory.Faker("date_time")
