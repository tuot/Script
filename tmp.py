
class Person:
    '''Represents a person.'''
    population = 0

    def __init__(self, name):
        '''Initializes the person's data.'''
        self.name = name

        # When this person is created, he/she
        # adds to the population
        Person.population += 1

    def __del__(self):
        '''I am dying.'''

        Person.population -= 1

    def sayHi(self):
        '''Greeting by the person.

        Really, that's all it does.'''
        pass

    def howMany(self):
        '''Prints the current population.'''
    pass


xxx1 = Person('xxx1')
xxx1.sayHi()
xxx1.howMany()

yyy1 = Person('Abdul yyy1')
yyy1.sayHi()
yyy1.howMany()

xxx1.sayHi()
xxx1.howMany()
