import csv
import textwrap

result = 'result.txt'

students_csv = 'backend-assessment/students.csv'
courses_csv = 'backend-assessment/courses.csv'
tests_csv = 'backend-assessment/tests.csv'
marks_csv = 'backend-assessment/marks.csv'

students = {}
courses = {}
tests = {}
marks = {}

# reading all csv files and converting them to dictionaries
with open(students_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skips the first line containing title
    for row in reader:
        # skips blank lines containing no data or lines with data missing in some columns
        if all(x.strip() for x in row):
            students[row[0]] = row[1]

with open(courses_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skips the first line containing title
    for row in reader:
        # skips blank lines containing no data or lines with data missing in some columns
        if all(x.strip() for x in row):
            courses[row[0]] = {'name': row[1], 'teacher': row[2]}

with open(tests_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skips the first line containing title
    for row in reader:
        # skips blank lines containing no data or lines with data missing in some columns
        if all(x.strip() for x in row):
            item = tests.get(row[1], dict())
            # discards negative entries for weight
            if int(row[2]) >= 0:
                item[row[0]] = int(row[2])
            tests[row[1]] = item
with open(marks_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skips the first line containing title
    for row in reader:
        # skips blank lines containing no data or lines with data missing in some columns
        if all(x.strip() for x in row):
            item = marks.get(row[1], dict())
            # discards negative entries for marks
            if int(row[2]) >= 0:
                item[row[0]] = int(row[2])
            marks[row[1]] = item

# deletes entries in tests whose tests account for less than 100% of course credit
to_delete = []
for k1, v1 in tests.items():
    weight_sum = 0
    for k2, v2 in v1.items():
        weight_sum += v2
    if weight_sum != 100:
        to_delete.append(k1)

for item in to_delete:
    del tests[item]

# generates student report cards
class Report:

    def __init__(self, id, student_name, avg):
        self.id = id
        self.student_name = student_name
        self.avg = avg
        self.course_list = []

    def course(self, course_name, teacher, grade):
        course_report = Course_Report(course_name, teacher, grade)
        self.course_list.append(course_report)

    def generate(self):
        with open(result, 'a') as f:
            f.write("Student Id: {}, name: {}\n".format(self.id, self.student_name))
            f.write("Total Average:     {:.2f}%\n\n".format(self.avg))
            for value in self.course_list:
                f.write(textwrap.indent("Course: {}, Teacher: {}\n".format(value.course_name, value.teacher), '   '))
                f.write(textwrap.indent("Final Grade:   {:.2f}%\n\n".format(value.grade), '   '))
            f.write("\n\n")

# generates individual course report depending on the number of courses a student has taken
class Course_Report:
    def __init__(self, course_name, teacher, grade):
        self.course_name = course_name
        self.teacher = teacher
        self.grade = grade

# loops over each student and computes course grade and total average
for k1 in sorted(marks.keys()):
    student_marks = marks.get(k1)
    avg = 0
    report_card = Report(k1, students.get(k1), avg)
    for k2 in tests:
        course_tests = tests.get(k2)
        grade = 0
        if set(student_marks.keys()).issuperset(set(course_tests.keys())):
            for k3 in course_tests:
                grade += course_tests.get(k3) * student_marks.get(k3) * 0.01
            report_card.course(courses[k2]['name'], courses[k2]['teacher'], grade)
            avg += grade
    avg = avg / len(report_card.course_list)
    report_card.avg = avg
    report_card.generate()