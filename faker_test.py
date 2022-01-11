from faker import Faker
import faker


faker = Faker()

res = faker.text(max_nb_chars=2000)
res = res[:300]


print(res)
print(len(res))

import random

# random.seed(10)
x = random.random()
print(x)

# random.seed(10)
y = random.random()
print(y)
