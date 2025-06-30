import factory

from bitrix_downloader.common.entities.bitrix import BitrixWorldModel


class BitrixWorldModelFactory(factory.Factory):
    class Meta:
        model = BitrixWorldModel

    id = factory.Sequence(lambda n: n)
    assigned_by_id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    first_name = factory.Faker("word")
    last_name = factory.Faker("word")
    age = factory.Faker("word")
    gender = factory.Sequence(lambda n: n)
    date_of_birth = factory.Faker("word")
    alabuga_start_simulation = factory.Sequence(lambda n: n)
    rejection = factory.Sequence(lambda n: n)
    citizenship_form = factory.Sequence(lambda n: n)
    passport = factory.Sequence(lambda n: n)
    passport_issue_date = factory.Faker("word")
    hundred_words = factory.Sequence(lambda n: n)
    first_touch_date = factory.Faker("word")
    upload_date = factory.Faker("word")
    project = factory.Sequence(lambda n: n)
