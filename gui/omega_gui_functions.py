from PyQt5.QtWidgets import QFileDialog
import yaml


def new_file_action(var1, var2):
    """
    Doc Stub
    """
    print(var1, var2)


def open_file_action(filepath):
    data = yaml_loader(filepath)
    # print(data)
    parts = data.get('input_files')
    for item_name, item_value in parts.items():
        print(item_name, item_value)
    parts = data.get('output_files')
    for item_name, item_value in parts.items():
        print(item_name, item_value)
    return data

    # g = data.get("input_files", "")
    # print(g)

    # a = data['file_1']
    # print(a)
    # data['file_1'] = "hello"
    # print(data['file_1'])

    # filepath2 = "test3.om2"
    # yaml_dump(filepath2, data)


def yaml_loader(filepath):
    """Loads a yaml file"""
    with open(filepath, "r") as file_descriptor:
        data = yaml.full_load(file_descriptor)
    return data


def yaml_dump(filepath, data):
    """Dumps data to a yaml file"""
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


        yaml.dump(data)

    print("Open File")


def save_file_action(file_name):
    """
    Doc Stub
    """

    dialog = QFileDialog()
    dialog.selectFile("der.jpg")
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setNameFilter(file_name)
    dialog.setViewMode(QFileDialog.Detail)
    if dialog.exec_():
        file_name = dialog.selectedFiles()
        file_name = str(file_name)[2:-2]
        return file_name


# def save_file_as_action(file_name, file_type):
    # print("Save File As")


def file_dialog(file_name, file_type, file_dialog_title):
    """
    Opens a file dialog to select a file with extension options.

    :param file_name: Default file name
    :param file_type: Specifies extension filter type
    :param file_dialog_title: Title for dialog box
    ...
    :return file_name: User selected file name
    :return file_type: Echo input param
    :return file_dialog_title: Echo input param
    """
    dialog = QFileDialog()
    dialog.selectFile(file_name)
    dialog.setWindowTitle(file_dialog_title)
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setNameFilter(file_type)
    dialog.setViewMode(QFileDialog.Detail)
    temp = dialog.selectedFiles()
    if dialog.exec_():
        file_name = dialog.selectedFiles()
        file_name = str(file_name)[2:-2]
        return file_name, file_type, file_dialog_title
    else:
        file_name = ""
        return file_name, file_type, file_dialog_title




