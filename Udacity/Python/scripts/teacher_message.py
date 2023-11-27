names = list(map(str.strip, input("Enter names separated by commas: ").title().split(",")))
assignments = list(map(int, map(str.strip, input("Enter assignment counts separated by commas: ").split(","))))
grades = list(map(float, map(str.strip, input("Enter grades separated by commas: ").split(","))))

message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

for name, assignment, grade in zip(names, assignments, grades):
    print(message.format(name, assignment, int(grade), int(grade) + (2*assignment)))