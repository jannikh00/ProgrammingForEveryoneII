# Python program that has a class called Person + two subclasses, Student and Staff
# Below the classes there's a small test of the functionality

# Person class
class Person:
    def __init__(self, name, age, country):
        self.name = name
        self.age = age
        self.country = country

    def introduce_yourself(self):
        print(f"Hello, my name is {self.name}. I'm {self.age} years old, and I'm from {self.country}.")

# Student subclass
class Student(Person):
    def __init__(self, name, age, country, major, gpa):
        super().__init__(name, age, country)
        self.major = major
        self.gpa = gpa

    def study(self):
        print(f"{self.name} is studying {self.major} with a current GPA of {self.gpa}.")

# Staff subclass
class Staff(Person):
    def __init__(self, name, age, country, position, department):
        super().__init__(name, age, country)
        self.position = position
        self.department = department

    def work(self):
        print(f"{self.name} works as a {self.position} in the {self.department} department.")

# tests of functionality of methods
person1 = Person("Leon", 21, "Poland")
student1 = Student("Daniel", 22, "Netherlands", "business administration", 3.8)
staff1 = Staff("Peter", 47, "USA", "head", "IT")
person1.introduce_yourself()
student1.introduce_yourself()
staff1.introduce_yourself()
student1.study()
staff1.work()