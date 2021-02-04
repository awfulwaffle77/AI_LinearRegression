import os

# TODO: Numarul de comentarii, nr de linii din README, normalizarea nr de linii de cod intr-un interval [0,1]

PATH = "F:\\Projects\\Python\\IA\\Tema2\\train"  # Path-ul in care se afla lucrarile studentilor
GRADES_PATH = "F:\\Projects\\Python\\IA\\Tema2"  # In ce folder se afla labels.txt

# Daca vreau sa printez un student si al catelea sa fie
PRINT = True
_INDEX = 0

def find_classes_path(student):
    for subdir, dirs, files in os.walk(PATH + "\\" + student):
        for file in files:
            if ".cpp" in file:
                return subdir


def find_readme_path(student):
    for subdir, dirs, files in os.walk(PATH + "\\" + student):
        for file in files:
            if "read" in file and ".txt" in file:
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
        if "read" in std.lower():
            # readme.append(std.split("\\")[-3].split("_")[1])
            readme = 1

    return readme


def check_interface(std, interfaces, virtual_functions):
    if ".h" in std:  # verificam numai dupa headere
        # Daca prima litera este i si urmaotarea este majuscula (ex. IDrawable sau iDraw)
        if std.split("\\")[-1][0].lower() == "i" and std.split("\\")[-1][1].isupper():
            virtual_functions += check_virtual_functions(std)
            interfaces += 1
    return interfaces, virtual_functions


def trace_files(path, diagram_path):  # returneaza o lista cu studentii care au interfete
    interfaces = 0
    virtual_functions = 0
    classes = 0
    diagrams = 0
    lines = 0
    _path = path + "\\"
    # Am presupus ca acele clase al caror nume incepe cu I este interfata si a doua litera este neaparat majuscula
    for std in os.listdir(path):  # parcurge folderul pentru student cu .cpp si .h
        try:
            interfaces, virtual_functions = check_interface(_path + std, interfaces, virtual_functions)
            classes = check_classes(_path + std, classes)

            lines += get_lines(_path + std)
        except:
            pass

    if diagram_path is not None:
        diagrams = 1
    return interfaces, virtual_functions, classes, diagrams, lines


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


def write_training_csv(student_list, grades_dict):
    diagram_path = find_diagram_path(student_list[_INDEX])  # unii studenti aveau doar poze, altii  doar .cd
    f = open("training.csv", "w")
    f.write("Student,Grade,Readme,Interfaces,Virt_functions,Classes,Diagrams,Lines")
    f.write("\n")

    for student in student_list:
        if str(student) in grades_dict:
            readme_path = find_readme_path(student)
            path = find_classes_path(student)
            trace = trace_files(path, diagram_path)
            f.write(str(student))
            f.write(",".rstrip('\n'))
            f.write(str(grades_dict[student]))
            f.write(",".rstrip('\n'))
            f.write(str(check_readme(readme_path)).rstrip('\n'))
            f.write(",".rstrip('\n'))
            f.write(str(trace[0]).rstrip('\n'))
            f.write(",".rstrip('\n'))
            f.write(str(trace[1]).rstrip('\n'))
            f.write(",".rstrip('\n'))
            f.write(str(trace[2]).rstrip('\n'))
            f.write(",".rstrip('\n'))
            f.write(str(trace[3]).rstrip('\n'))
            f.write(",".rstrip('\n'))
            f.write(str(trace[4]))
            f.write("\n")


def write_test_csv(student_list):
    diagram_path = find_diagram_path(student_list[_INDEX])  # unii studenti aveau doar poze, altii  doar .cd
    f = open("test.csv", "w")
    f.write("Student,Readme,Interfaces,Virt_functions,Classes,Diagrams,Lines")
    f.write("\n")

    for student in student_list:
        readme_path = find_readme_path(student)
        path = find_classes_path(student)
        trace = trace_files(path, diagram_path)
        f.write(str(student))
        f.write(",".rstrip('\n'))
        f.write(str(check_readme(readme_path)).rstrip('\n'))
        f.write(",".rstrip('\n'))
        f.write(str(trace[0]).rstrip('\n'))
        f.write(",".rstrip('\n'))
        f.write(str(trace[1]).rstrip('\n'))
        f.write(",".rstrip('\n'))
        f.write(str(trace[2]).rstrip('\n'))
        f.write(",".rstrip('\n'))
        f.write(str(trace[3]).rstrip('\n'))
        f.write(",".rstrip('\n'))
        f.write(str(trace[4]))
        f.write("\n")


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
        print("Interfaces: ", trace[0])
        print("Virt funcs: ", trace[1])
        print("Classes: ", trace[2])
        print("Diagrams : ", trace[3])
        print("Lines : ", trace[4])

    if PATH.split("\\")[-1] == "train":
        write_training_csv(student_list, grades_dict)
    elif PATH.split("\\")[-1] == "test":
        write_test_csv(student_list)
