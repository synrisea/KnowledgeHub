class Human:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def show_info(self):
        return f"{self.first_name} {self.last_name} {self.age}"


class Student(Human):
    def __init__(self, first_name, last_name, age, group, mark):
        super().__init__(first_name, last_name, age)
        self.group = group
        self.mark = mark

    def show_info(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.group} {self.mark}"

def foo(obj: Human):
    print(obj.show_info())


student = Student("John", "Smith", 24, True, 12)
human = Human("Nadir", "Zamanov", 45)

foo(human)
foo(student)


