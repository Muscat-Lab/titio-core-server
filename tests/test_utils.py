import faker

f = faker.Faker()


def generate_random_email():
    return f.email()
