import os
from zipfile import ZipFile, ZIP_DEFLATED

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStorageInfo, QFile, QIODevice, QTextStream, QJsonParseError, QJsonDocument, QJsonValue, \
    QByteArray, QXmlStreamWriter, QXmlStreamReader, QFileInfo
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from ui.mainwindow import Ui_MainWindow
import sys


class Student(object):
    def __init__(self, fio, year, track):
        self.fio = fio
        self.year = year
        self.track = track

    def getFio(self):
        return self.fio

    def getYear(self):
        return self.year

    def getTrack(self):
        return self.track

class Discipline(object):
    def __init__(self, title, year, teacher):
        self.title = title
        self.year = year
        self.teacher = teacher

    def __init__(self):
        pass

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getYear(self):
        return self.year

    def setYear(self, year):
        self.year = year

    def getTeacher(self):
        return self.teacher

    def setTeacher(self, teacher):
        self.teacher = teacher

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.students_list = []
        self.disciplines_list = []
        self.pathToZip = ""
        self.files_paths = []

        self.get_sys_info()

        self.ui.pushButton.clicked.connect(self.safe_file)
        self.ui.pushButton_2.clicked.connect(self.open_file)
        self.ui.pushButton_3.clicked.connect(self.del_file)

        self.ui.pushButton_4.clicked.connect(self.save_json)
        self.ui.pushButton_5.clicked.connect(self.open_json)
        self.ui.pushButton_6.clicked.connect(self.add_json_obj)

        self.ui.pushButton_7.clicked.connect(self.add_xml_obj)
        self.ui.pushButton_8.clicked.connect(self.open_xml)
        self.ui.pushButton_9.clicked.connect(self.save_xml)

        self.ui.pushButton_10.clicked.connect(self.open_zip)
        self.ui.pushButton_11.clicked.connect(self.unzip)
        self.ui.pushButton_12.clicked.connect(self.add_file_to_zip)
        self.ui.pushButton_13.clicked.connect(self.zip)






    def get_sys_info(self):
        for storage in QStorageInfo.mountedVolumes():
            if (storage.isValid()) & (storage.isReady()):
                if (not storage.isReadOnly()):
                    self.ui.listWidget.addItem(f"раздел:  {str(storage.device(),'utf-8')} \nname: {storage.displayName()} \nsize: {int(storage.bytesTotal() / 1000 / 1000)} МБ\navaliable size: {int(storage.bytesAvailable() / 1000 / 1000)} МБ\nfileSystemType: {str(storage.fileSystemType(), 'utf-8')}\n")


    def safe_file(self):
        fileName, check = QFileDialog.getSaveFileName(self, "сохранить", "~/", "txt files (*.txt)")
        if(not check):
            return
        file = QFile(fileName)

        if (not file.open(QIODevice.ReadWrite)):
            QMessageBox.information(0, "error", file.errorString())
            return

        stream = QTextStream(file)
        stream << self.ui.plainTextEdit.toPlainText()
        stream.flush()

        file.close()


    def open_file(self):
        fileName, check = QFileDialog.getOpenFileName(self, "открыть", "~/", "text files (*.txt)")

        if(not check):
            return

        file = QFile(fileName)

        if (not file.open(QIODevice.ReadOnly)):
            QMessageBox.information(0, "error", file.errorString())
            return

        stream = QTextStream(file)

        while (not stream.atEnd()):
            line = stream.readLine() + '\n'
            self.ui.plainTextEdit.insertPlainText(line)

        file.close()


    def del_file(self):
        fileName, check = QFileDialog.getOpenFileName(self, "открыть", "~/", "text files (*.txt)")

        if(not check):
            return

        os.remove(fileName)

    def open_json(self):
        self.ui.listWidget_2.clear()
        self.students_list.clear()

        fileName, check = QFileDialog.getOpenFileName(self, "открыть", "~/", "json files (*.json)")

        if(not check):
            return

        file = QFile(fileName)
        file.open(QIODevice.ReadOnly | QIODevice.Text)
        val = file.readAll()
        file.close()


        error = QJsonParseError()

        doc = QJsonDocument.fromJson(val, error)

        if (doc.isObject()):
                json = doc.object()
                jsonArray = json["students"].toArray()
                for value in jsonArray:
                    if (value.isObject()):
                        obj = value.toObject();
                        fio = obj["name"].toString();
                        year = obj["year"].toString();
                        track = obj["track"].toString();

                        self.students_list.append(Student(fio, year, track));
                        self.ui.listWidget_2.addItem(f"ФИО: {fio} \nГод поступления: {year} \nНаправление: {track}\n");



    def save_json(self):
        fileName, check = QFileDialog.getSaveFileName(self, "сохранить", "~/", "json files (*.json)")

        if(not check):
            return

        data = QByteArray()
        json = QJsonDocument.fromJson(data).object()

        jsonarry = QJsonDocument.fromJson(data).array()
        for item in self.students_list:
            jsontems = QJsonDocument.fromJson(data).object()
            jsontems["name"] = str(item.getFio())
            jsontems["year"] = str(item.getYear())
            jsontems["track"] = str(item.getTrack())
            jsonarry.append(jsontems)

        json["students"] = jsonarry

        outputjson = QJsonDocument(json).toJson(QJsonDocument.Indented)

        file = QFile(fileName)
        file.open(QIODevice.WriteOnly | QIODevice.Text)
        stream = QTextStream(file)
        stream << outputjson
        stream.flush()
        file.close()

    def add_json_obj(self):
        self.students_list.append(Student(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text()))
        self.ui.listWidget_2.addItem("ФИО: " + self.ui.lineEdit.text() + "\nГод поступления: " + self.ui.lineEdit_2.text() + "\nНаправление: " + self.ui.lineEdit_3.text() + "\n")


    def open_xml(self):
        self.ui.listWidget_3.clear()
        self.disciplines_list.clear()

        fileName, check = QFileDialog.getOpenFileName(self, "открыть", "~/", "xml files (*.xml)")

        if(not check):
            return


        file = QFile(fileName)
        if (not file.open(QFile.ReadOnly | QFile.Text)):

            QMessageBox.warning(self,"Ошибка файла","Не удалось открыть файл",QMessageBox.Ok)
            return


        xmlReader = QXmlStreamReader(file)

        xmlReader.readNext()

        while (not xmlReader.atEnd()):
            if (xmlReader.isStartElement()):
                if (xmlReader.name() == "title"):
                    discipline = Discipline()
                    discipline.setTitle(xmlReader.readElementText())

                elif (xmlReader.name() == "year"):
                    discipline.setYear(xmlReader.readElementText())

                elif (xmlReader.name() == "teacher"):

                    discipline.setTeacher(xmlReader.readElementText())

                    self.ui.listWidget_3.addItem(f"Название: {discipline.getTitle()}\nГод утверждения: {discipline.getYear()}\nПреподаватель: {discipline.getTeacher()}\n")
                    self.disciplines_list.append(discipline)

            xmlReader.readNext()

        file.close()



    def save_xml(self):
        fileName,check = QFileDialog.getSaveFileName(self, "сохранить", "~/", "xml files (*.xml)")

        if(not check):
            return

        file = QFile(fileName)
        file.open(QIODevice.WriteOnly)


        xmlWriter = QXmlStreamWriter(file)
        xmlWriter.setAutoFormatting(True)
        xmlWriter.writeStartDocument()

        xmlWriter.writeStartElement("disciplins");
        for item in self.disciplines_list:
                xmlWriter.writeStartElement("disciplin")

                xmlWriter.writeStartElement("title")
                xmlWriter.writeCharacters(item.getTitle());
                xmlWriter.writeEndElement();

                xmlWriter.writeStartElement("year")
                xmlWriter.writeCharacters(item.getYear());
                xmlWriter.writeEndElement()

                xmlWriter.writeStartElement("teacher")
                xmlWriter.writeCharacters(item.getTeacher())
                xmlWriter.writeEndElement()

                xmlWriter.writeEndElement()


        xmlWriter.writeEndElement()
        xmlWriter.writeEndDocument()
        file.close();

    def add_xml_obj(self):
        self.disciplines_list.append(Discipline(self.ui.lineEdit_4.text(), self.ui.lineEdit_5.text(), self.ui.lineEdit_6.text()))
        self.ui.listWidget_3.addItem(f"название: {self.ui.lineEdit_4.text()} \nГод утверждения: {self.ui.lineEdit_5.text()}\nПреподаватель: {self.ui.lineEdit_6.text()} \n");

    def add_file_to_zip(self):
        self.pathToZip = "";
        self.ui.pushButton_11.setEnabled(False);
        self.ui.pushButton_13.setEnabled(True);

        fileName,check = QFileDialog.getOpenFileName(self, "открыть", "~/")

        if(not check):
            return

        self.files_paths.append(fileName)

        self.ui.listWidget_4.addItem(f"Файл: {QFileInfo(fileName).fileName()}\nПуть: {fileName}\nРазмер: {QFileInfo(fileName).size()}");

    def open_zip(self):
        self.ui.listWidget_4.clear()
        self.files_paths.clear()
        self.ui.pushButton_11.setEnabled(True)
        self.ui.pushButton_13.setEnabled(False)

        fileName, check = QFileDialog.getOpenFileName(self, "открыть", "~/", "zip files (*.zip)")

        if(not check):
            return

        with ZipFile(fileName, "r") as myzip:
            self.pathToZip = fileName
            self.ui.listWidget_4.addItem(f"количество файлов в архиве - {len(myzip.infolist())}")
            for item in myzip.infolist():
                self.ui.listWidget_4.addItem(f"Название: {item.filename} размер: {item.file_size} байт")

        self.ui.pushButton_11.setEnabled(True)

    def unzip(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory", "/home", QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks);
        with ZipFile(self.pathToZip, "r") as myzip:
            myzip.extractall(path=dir)

    def zip(self):
        fileName,check = QFileDialog.getSaveFileName(self, "сохранить", "~/", "zip files (*.zip)")

        if(not check):
            return

        with ZipFile(fileName, "w", compression=ZIP_DEFLATED, compresslevel=3) as myzip:
            for item in self.files_paths:
                myzip.write(item, QFileInfo(item).fileName())


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())