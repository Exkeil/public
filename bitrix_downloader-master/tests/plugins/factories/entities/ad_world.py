import factory

from bitrix_downloader.common.entities.bitrix import AdWorldModel


class AdWorldModelFactory(factory.Factory):
    class Meta:
        model = AdWorldModel

    id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    source_id = factory.Sequence(lambda n: f"source_id{n}")
    name = factory.Faker("word")
    surname = factory.Faker("word")
