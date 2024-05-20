# Python program that includes an example of polymorphism

# Parent class "Student"
class Student:
    def __init__(self, name, major, gpa_for_semesters):
        self.name = name
        self.major = major
        self.gpa_for_semesters = gpa_for_semesters

    def study(self):
        print(f"{self.name} is studying {self.major}.")

    def calculate_average_gpa(self):
        sum = 0
        for i in self.gpa_for_semesters:
            sum += i
        gpa = round(sum/len(self.gpa_for_semesters), 2)
        return gpa
    
    def is_in_good_standings(self):
        print(f"{self.name} is a student.")

# Child Class "UndergraduateStudent" that overrides functions study() and is_in_good_standings()
class UndergraduateStudent(Student):

    def study(self):
        print(f"{self.name} is studying {self.major} using lectures and textbooks.")

    def is_in_good_standings(self):
        sum = 0
        for i in self.gpa_for_semesters:
            sum += i
        gpa = round(sum/len(self.gpa_for_semesters), 2)
        if gpa >= 2.5:
            return print(f"{self.name} is in good academic standing.")
        elif gpa < 2.5:
            print(f"{self.name} is not in good academic standing.")

# Child Class "GraduateStudent" that overrides functions study() and is_in_good_standings()
class GraduateStudent(Student):
    
    def study(self):
        print(f"{self.name} is studying {self.major} through research papers and projects.")

    def is_in_good_standings(self):
        sum = 0
        for i in self.gpa_for_semesters:
            sum += i
        gpa = round(sum/len(self.gpa_for_semesters), 2)
        if gpa >= 3.0:
            return print(f"{self.name} is in good academic standing.")
        elif gpa < 3.0:
            print(f"{self.name} is not in good academic standing.")

###########################################################################################################

# main program
gpa_list = [2.4, 3.0, 3.5]
undergrad1 = UndergraduateStudent("Max", "Business Administration", gpa_list)
grad1 = GraduateStudent("Colin", "Computer Science", gpa_list)
for x in (undergrad1, grad1):
    x.study()
    print(x.calculate_average_gpa())
    x.is_in_good_standings()