class Human:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    # def __repr__(self):
    #     return "class <Human>"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age}"

    def __int__(self):
        return len(self.first_name)

    def __add__(self, other):
        return self.age + other.age

    def __eq__(self, other):
        return  self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def __gt__(self, other):
        return self.age > other.age

    def __le__(self, other):
        return self.age <= other.age

    def __ge__(self, other):
        return self.age >= other.age

    def __len__(self):
        return len(self.first_name)




# a = 5
#
# print(type(a))
# print(str(a))

# human = Human("Nadir", "Zamanov", 45)
# human1 = Human("Salamata", "Salamzade", 35)
# print(human)
#
# print(str(human))
# print(int(human))
# print(human + human1)
# print(human == human1)
# print(human >= human1)
# print(len(human1))



