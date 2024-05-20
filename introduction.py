# very simple Python program that contains the class Person and tests it's only method with two examples
# Moreover I've added one more attribute and one method, that displays the fourth attribute: height in cm

class Person:

    def __init__(self, name, age, country, height):
        self.name = name
        self.age = age
        self.country = country
        self.height = height

    def introduce_yourself(self):
        print(f"Hello, my name is {self.name}. I'm {self.age} years old and I'm from {self.country}.")

    def height_output(self):
        print(f"{self.name} is {self.height}cm tall.")

person1 = Person("John", 30, "Canada", 187)
person2 = Person("Maria", 25, "Spain", 169)

person1.introduce_yourself()
person2.introduce_yourself()
person1.height_output()
person2.height_output()


    