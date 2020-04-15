import random


class House():
    def set_person(self, person):
        if person:
            person.house = self
        self.person = person

    def order_text(self):
        return {
            0: 'first',
            1: 'second',
            2: 'third',
            3: 'fourth',
            4: 'fifth',
        }.get(self.order, 'unknown')

    def __init__(self, person=None, color=None):
        self.set_person(person)
        self.color = color
        # 0 is on far left, 4 is on far right
        self.order = None

    def __repr__(self):
        attrs = [
            self.order_text(),
            self.color,
            self.person.nationality,
            self.person.beverage,
            self.person.cigar,
            self.person.pet,
        ]
        padded_attrs = [f"{attr:12}" for attr in attrs]
        return " ".join(padded_attrs)

    def __str__(self):
        return self.__repr__()


class Person():
    def set_house(self, house):
        if house:
            house.person = self
        self.house = house

    def __init__(self, nationality=None, beverage=None, cigar=None, pet=None):
        self.nationality = nationality
        self.beverage = beverage
        self.cigar = cigar
        self.pet = pet
        self.house = None

    def __repr__(self):
        return f"{self.nationality}, drinks {self.beverage or 'nothing'}, smokes {self.cigar or 'nothing'}, has {self.pet or 'no pet'}"

    def __str__(self):
        return self.__repr__()


class Simulation():
    def __init__(self):
        self.init()

    def init(self):
        self.generate_houses()
        self.generate_people()
        self.add_people_to_houses()
        self.apply_rules()

    def __repr__(self):
        houses_in_order = sorted(self.houses, key=lambda h: h.order)
        return "\n".join([str(house) for house in houses_in_order])

    def __str__(self):
        return self.__repr__()

    def shuffle(self, objects):
        return random.sample(objects, len(objects))

    def generate_houses(self):
        colors = self.shuffle(["red", "white", "green", "yellow", "blue"])
        orders = self.shuffle([0, 1, 2, 3, 4])

        self.houses = [House(color=color) for color in colors]
        for index, order in enumerate(orders):
            self.houses[index].order = order

    def generate_people(self):
        nationalities = self.shuffle(["British", "Swedish", "Danish", "Norwegian", "German"])
        beverages = self.shuffle(["tea", "coffee", "milk", "beer", "water"])
        cigars = self.shuffle(["pall mall", "bluemaster", "prince", "blend", "dunhill"])
        pets = self.shuffle(["dog", "cat", "horse", "bird", "fish"])

        self.people = [Person(nationality=nationality) for nationality in nationalities]
        for index, beverage in enumerate(beverages):
            self.people[index].beverage = beverage
        for index, cigar in enumerate(cigars):
            self.people[index].cigar = cigar
        for index, pet in enumerate(pets):
            self.people[index].pet = pet

    def add_people_to_houses(self):
        random_people = self.shuffle(self.people)
        for index, person in enumerate(random_people):
            self.houses[index].set_person(person)

    def get_person_by_nationality(self, nationality):
        return next((person for person in self.people if person.nationality == nationality), None)

    def get_person_by_beverage(self, beverage):
        return next((person for person in self.people if person.beverage == beverage), None)

    def get_person_by_cigar(self, cigar):
        return next((person for person in self.people if person.cigar == cigar), None)

    def get_person_by_pet(self, pet):
        return next((person for person in self.people if person.pet == pet), None)

    def get_person_by_house_color(self, house_color):
        return next((person for person in self.people if person.house.color == house_color), None)

    def get_house_by_color(self, color):
        return next((house for house in self.houses if house.color == color), None)

    def get_house_by_order(self, order):
        return next((house for house in self.houses if house.order == order), None)

    def switch_houses(self, p1, p2):
        h1 = p1.house
        h2 = p2.house
        p1.set_house(h2)
        p2.set_house(h1)

    def assign_item(self, person, item_name, item_value):
        old_item = getattr(person, item_name)
        getter = getattr(self, f"get_person_by_{item_name}")
        other_person = getter(item_value)
        setattr(other_person, item_name, old_item)
        setattr(person, item_name, item_value)

    def apply_rules(self):
        if self.get_person_by_nationality('British').house.color != 'red':
            self.switch_houses(self.get_person_by_nationality('British'), self.get_person_by_house_color('red'))
        self.assign_item(self.get_person_by_nationality('Swedish'), 'pet', 'dog')
        self.assign_item(self.get_person_by_nationality('Danish'), 'beverage', 'tea')
        self.assign_item(self.get_house_by_color('green').person, 'beverage', 'coffee')
        self.assign_item(self.get_person_by_cigar('pall mall'), 'pet', 'bird')
        self.assign_item(self.get_house_by_color('yellow').person, 'cigar', 'dunhill')
        self.assign_item(self.get_house_by_order(2).person, 'beverage', 'milk')
        self.assign_item(self.get_house_by_order(0).person, 'nationality', 'Norwegian')
        self.assign_item(self.get_person_by_cigar('bluemaster'), 'beverage', 'beer')
        self.assign_item(self.get_person_by_nationality('German'), 'cigar', 'prince')

    def is_valid(self):
        # the Brit lives in the red house
        if self.get_person_by_nationality('British').house.color != 'red':
            return False
        # the Swede keeps dogs as pets
        if self.get_person_by_nationality('Swedish').pet != 'dog':
            return False
        # the Dane drinks tea
        if self.get_person_by_nationality('Danish').beverage != 'tea':
            return False
        # the green house is on the left of the white house
        if self.get_house_by_color('green').order + 1 != self.get_house_by_color('white').order:
            return False
        # the green house's owner drinks coffee
        if self.get_house_by_color('green').person.beverage != 'coffee':
            return False
        # the person who smokes Pall Mall rears birds
        if self.get_person_by_cigar('pall mall').pet != 'bird':
            return False
        # the owner of the yellow house smokes Dunhill
        if self.get_house_by_color('yellow').person.cigar != 'dunhill':
            return False
        # the man living in the center house drinks milk
        if self.get_house_by_order(2).person.beverage != 'milk':
            return False
        # the Norwegian lives in the first house
        if self.get_house_by_order(0).person.nationality != 'Norwegian':
            return False
        # the man who smokes blends lives next to the one who keeps cats
        if abs(self.get_person_by_cigar('blend').house.order - self.get_person_by_pet('cat').house.order) != 1:
            return False
        # the man who keeps horses lives next to the man who smokes Dunhill
        if abs(self.get_person_by_pet('horse').house.order - self.get_person_by_cigar('dunhill').house.order) != 1:
            return False
        # the owner who smokes BlueMaster drinks beer
        if self.get_person_by_cigar('bluemaster').beverage != 'beer':
            return False
        # the German smokes Prince
        if self.get_person_by_nationality('German').cigar != 'prince':
            return False
        # the Norwegian lives next to the blue house
        if abs(self.get_person_by_nationality('Norwegian').house.order - self.get_house_by_color('blue').order) != 1:
            return False
        # the man who smokes blend has a neighbor who drinks water
        if abs(self.get_person_by_cigar('blend').house.order - self.get_person_by_beverage('water').house.order) != 1:
            return False

        return True


def main():
    max_attempts = 100000
    success = False
    sim = Simulation()

    for i in range(0, max_attempts):
        if sim.is_valid():
            print(f"Found solution after {i} attempts")
            print(sim)
            success = True
            sim.init()
            break
        else:
            sim.init()

    if not success:
        print(f"Gave up after {max_attempts} attempts")


if __name__ == '__main__':
    main()
