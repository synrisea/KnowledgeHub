class Human:
    # name = "Nadir"
    # surname = "Zamanov"
    __count = 0
    def __init__(self, name, surname, age, mark):
        self.name = name                    # public
        self.surname = surname              # public
        self.__age = age if age > 0 else 0  #private
        self._mark = mark                   #protected
        Human.__count += 1

    def show_info(self):
        print(self.name, self.surname, self.age, self.mark)

    # def initialize(self, name, surname, age, mark):
    #     self.name = name
    #     self.surname = surname
    #     self.age = age
    #     self.mark = mark

    # def get_age(self):
    #     return self.__age
    #
    # def set_age(self, age):
    #     self.__age = age if age > 0 else 0

    # python property
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value if value > 0 else 0

    @staticmethod
    def show_count():
        return Human.__count

# human = Human("Nadir", "Zamanov", 45, "Salam")
# print(Human.show_count())
# human1 = Human("Ridan", "Vonamaz", 54, 1)
# print(Human.show_count())
# print(human.age)
# human.age = 12
# print(human.age)
#
# print(human._mark)

# magic methods, Inheritance, "утиная типизация"



