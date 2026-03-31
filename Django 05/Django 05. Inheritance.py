class Human:
    def __init__(self, first_name, last_name, age):
        self._first_name = first_name
        self.last_name = last_name
        self.age = age


class Student(Human):
    def __init__(self, first_name, last_name, age, group, mark):
        super().__init__(first_name, last_name, age)
        self.group = group
        self.mark = mark

    def show_info(self):
        print(self._first_name)


student = Student(
    "Nadir",
    "Zamanov",
    45,
    "FSDE_1_24_3_ru",
    12
)

# student.show_info()

print(isinstance(student, Human))
print(isinstance(Student, Human))
print(isinstance(student, object))