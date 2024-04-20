import factory

from core.users.schemas import UserDTOCreateSchema


class UserDTOCreateFactory(factory.Factory):
    username = factory.Faker("user_name")
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    email = factory.Faker("email")
    phone_number = factory.Sequence(lambda n: "123-555-%04d" % n)
    password1 = "password"
    password2 = "password"

    class Meta:
        model = UserDTOCreateSchema
