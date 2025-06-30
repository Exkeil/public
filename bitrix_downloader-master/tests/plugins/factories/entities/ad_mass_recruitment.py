import factory

from bitrix_downloader.common.entities.bitrix import AdMassRecruitmentModel


class AdMassRecruitmentModelFactory(factory.Factory):
    class Meta:
        model = AdMassRecruitmentModel

    id = factory.Sequence(lambda n: n)
    stage_id = factory.Sequence(lambda n: f"stage_id{n}")
    source_id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    user_name = factory.Faker("word")
