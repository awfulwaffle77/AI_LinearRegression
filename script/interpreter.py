import os

PATH = "F:\\Projects\\Python\\IA\\LinearRegression\\test"  # Path-ul in care se afla lucrarile studentilor
GRADES_PATH = "F:\\Projects\\Python\\IA\\LinearRegression"  # In ce folder se afla labels.txt
PATH_TEST_CSV = "F:\\Projects\\Python\\IA\\LinearRegression\\csv\\test_4.csv"
PATH_TRAIN_CSV = "F:\\Projects\\Python\\IA\\LinearRegression\\csv\\training_4.csv"
CSV_HEADER = "Student,Grade,Readme,Interfaces,Virt_functions,Classes,Diagrams,Lines"

# Daca vreau sa printez un student si al catelea sa fie
PRINT = True
_INDEX = 0


class Student:
    def __init__(self, name, grade, readme, interfaces, vfuncs, classes, diagrams, lines):
        self.name = name
        if grade is None:
            self.grade = -1
        else:
            self.grade = grade
        self.readme = readme
        self.interfaces = interfaces
        self.vfuncs = vfuncs
        self.classes = classes
        self.diagrams = diagrams
        self.lines = lines


def find_classes_path(student):
    for subdir, dirs, files in os.walk(PATH + "\\" + student):
        for file in files:
            if ".cpp" in file:
                return subdir


def find_readme_path(student):
    for subdir, dirs, files in os.walk(PATH + "\\" + student):
        for file in files:
            # we discovered that some readmes are named RAED
            if "read" in file.lower() and ".txt" in file.lower() or "raed" in file.lower():
                return subdir


def find_diagram_path(student):
    for subdir, dirs, files in os.walk(PATH + "\\" + student):
        for file in files:
            if ".cd" in file or ".jpg" in file or ".png" in file or ".jpeg" in file:
                return subdir
    return None


def get_student_list():
    return os.listdir(PATH)


def check_readme(path):  # returneaza 1 daca are fisier de readme
    readme = 0
    for std in os.listdir(path):
        if "read" in std.lower() or "raed" in std.lower():
            readme = 1
            # Pentru normalizarea numarului de caractere din readme. Daca comentam partea asta, vom avea numai
            #       0 sau 1, daca are fisier de readme sau nu
            with open(path + "\\" + std, "r") as file:
                filename = file.read()
                readme = sum(len(word) for word in filename)
            #### Comenteaza pana aici

    return readme


def check_interface(std, interfaces, virtual_functions):
    if ".h" in std:  # verificam numai dupa headere
        # Daca prima litera este i si urmatoarea este majuscula (ex. IDrawable sau iDraw)
        if std.split("\\")[-1][0].lower() == "i" and std.split("\\")[-1][1].isupper():
            virtual_functions += check_virtual_functions(std)
            interfaces += 1
    return interfaces, virtual_functions


def trace_files(path, diagram_path):
    interfaces = 0
    virtual_functions = 0
    classes = 0
    diagrams = 0
    lines = 0
    _path = path + "\\"
    for std in os.listdir(path):  # parcurge folderul pentru student cu .cpp si .h
        try:
            interfaces, virtual_functions = check_interface(_path + std, interfaces, virtual_functions)
            classes = check_classes(_path + std, classes)

            lines += get_lines(_path + std)
        except:
            pass

    if diagram_path is not None:
        diagrams = 1

    return {"interfaces": interfaces, "vfuncs": virtual_functions, "classes": classes, "diagrams": diagrams,
                "lines": lines}


def check_virtual_functions(path):  # returneaza numarul functiilor virtuale
    virtual_functions = 0
    f = open(path, "r")
    for line in f.readlines():
        if "virtual" in line and "~" not in line:
            virtual_functions += 1
    return virtual_functions


def check_classes(std, classes):
    if ".cpp" in std:
        classes += 1
    return classes


def get_lines(std):
    if ".h" in std or ".cpp" in std:
        f = open(std, "r")
        return len(f.readlines())
    return 0


def read_grades():
    f = open(GRADES_PATH + "\\labels.txt", "r")
    dict = {}
    for line in f:
        splitted = line.split("\t\t")
        splitted[1] = splitted[1][:-1]  # stergem \n
        if splitted[1] == "NaN":  # ignoram studentii cu NaN
            continue
        dict[splitted[0]] = splitted[1]
    return dict


def write_to_csv(obj_std):
    if PATH.split("\\")[-1] == "test":
        filename = PATH_TEST_CSV
    elif PATH.split("\\")[-1] == "train":
        filename = PATH_TRAIN_CSV
    else:
        raise Exception("Wrong filename")

    f = open(filename, "w")
    f.write(CSV_HEADER)
    f.write("\n")
    for obj in obj_std:
        f.write(str(obj.name))
        f.write(",")
        f.write(str(obj.grade))
        f.write(",")
        f.write(str(obj.readme))
        f.write(",")
        f.write(str(obj.interfaces))
        f.write(",")
        f.write(str(obj.vfuncs))
        f.write(",")
        f.write(str(obj.classes))
        f.write(",")
        f.write(str(obj.diagrams))
        f.write(",")
        f.write(str(obj.lines))
        f.write("\n")


def get_students_as_obj(student_list, grades_dict):
    obj_student_list = []
    diagram_path = find_diagram_path(student_list[_INDEX])  # unii studenti aveau doar poze, altii  doar .cd
    for student in student_list:
        readme_path = find_readme_path(student)
        path = find_classes_path(student)
        trace = trace_files(path, diagram_path)
        if PATH.split("\\")[-1] == "test":  # studentii din test nu au nota, asa ca ii tratez diferit
            if not student in grades_dict:
                grade = None
            elif student in grades_dict:
                grade = grades_dict[student]
        elif PATH.split("\\")[-1] == "train":
            if student not in grades_dict:
                continue
            else:
                grade = grades_dict[student]
        obj_student_list.append(Student(student, grade, check_readme(readme_path), trace["interfaces"],
                                        trace["vfuncs"], trace["classes"], trace["diagrams"],
                                        trace["lines"]))
    return obj_student_list


def normalize_lines(obj_std):  # Rescaling (min-max normalization)
    max_lines = -1
    min_lines = 1000000
    # Comenteaza aici pentru a nu normaliza liniile din readme(in cazul in care ma intereseaza doar existenta readme)
    max_readme_chars = -1
    min_readme_chars = 1000000
    # Pana aici
    for obj in obj_std:
        if obj.lines > max_lines:
            max_lines = obj.lines
        if obj.lines < min_lines:
            min_lines = obj.lines
        # Comenteaza aici
        if obj.readme > max_readme_chars:
            max_readme_chars = obj.readme
        if obj.readme < min_readme_chars:
            min_readme_chars = obj.readme
        # Pana aici
    for obj in obj_std:
        obj.lines = (obj.lines - min_lines) / (max_lines - min_lines)
        # Comenteaza aici
        obj.readme = (obj.readme - min_readme_chars) / (max_readme_chars - min_readme_chars)
        # Pana aici


if __name__ == "__main__":

    student_list = get_student_list()
    grades_dict = read_grades()

    if PRINT:
        path = find_classes_path(student_list[_INDEX])
        diagram_path = find_diagram_path(student_list[_INDEX])  # unii studenti aveau doar poze, altii  doar .cd
        trace = trace_files(path, diagram_path)
        readme_path = find_readme_path(student_list[_INDEX])

        print(student_list)
        print("Path: ", path)
        print(student_list[_INDEX])
        print("README: ", check_readme(readme_path))
        print("Interfaces: ", trace["interfaces"])
        print("Virt funcs: ", trace["vfuncs"])
        print("Classes: ", trace["classes"])
        print("Diagrams : ", trace["diagrams"])
        print("Lines : ", trace["lines"])

    obj_std = get_students_as_obj(student_list, grades_dict)
    normalize_lines(obj_std)
    write_to_csv(obj_std)
