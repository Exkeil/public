import factory

from bitrix_downloader.common.entities.bitrix import AdSNGModel


class AdSNGModelFactory(factory.Factory):
    class Meta:
        model = AdSNGModel

    id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
    source_id = factory.Sequence(lambda n: f"source_id_{n}")
    surname = factory.Faker("word")
