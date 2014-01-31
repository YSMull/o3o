from PyQt4.QtGui import (QApplication, QDialog, QLabel, QHBoxLayout,QClipboard,
                    QLineEdit, QComboBox, QIcon, QGridLayout, QMessageBox)
from PyQt4.QtCore import (Qt, SIGNAL, QString)
from sys import (argv)
from json import (loads)



class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        data = self.getData()
        
        self.tags = data[0]
        self.yan  = data[1]
        self.give_copy_imformation = 1

        self.tag_label     = QLabel(u"&tag")
        self.LineEdit  = QLineEdit()
        self.tag_label.setBuddy(self.LineEdit)
        
        self.LineEdit2 = QLineEdit()
        self.LineEdit2.setVisible(False)

        self.yan_label    = QLabel(u'&yan')
        self.yan_ComboBox  = QComboBox()
        self.yan_label.setBuddy(self.yan_ComboBox)
        
        self.tag_ComboBox = QComboBox()
        
        
        editlayout = QHBoxLayout()
        editlayout.addWidget(self.LineEdit)
        editlayout.addWidget(self.LineEdit2)
        
        layout = QGridLayout()
        layout.addWidget(self.tag_label, 0, 0)
        layout.addLayout(editlayout, 0, 1)
        layout.addWidget(self.tag_ComboBox, 1, 1)
        
        layout.addWidget(self.yan_label, 2, 0)
        layout.addWidget(self.yan_ComboBox, 2, 1)
        
        
        self.tag_ComboBox.addItems(self.tags)
        
        self.setLayout(layout)
        self.setWindowTitle(u"o3o")
        self.setWindowIcon(QIcon('o3o.ico'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        
        self.set_yan_combobox()

        self.connect(self.LineEdit, SIGNAL("textChanged(QString)"), self.set_tag_combobox)
        self.connect(self.tag_ComboBox, SIGNAL("activated(QString)"), self.set_yan_combobox)
        self.connect(self.tag_ComboBox, SIGNAL("currentIndexChanged(QString)"), self.set_yan_combobox)
        self.connect(self.yan_ComboBox, SIGNAL("activated(QString)"), self.copy_text)
        self.connect(self.yan_ComboBox, SIGNAL("currentIndexChanged(QString)"), self.copy_text)
        self.connect(self.LineEdit, SIGNAL("returnPressed()"), self.popup)
        
        
    def popup(self):
        self.yan_ComboBox.showPopup()
        

    def copy_text(self):
        print 'set_text'

        self.LineEdit2.setText(self.yan_ComboBox.currentText())
        self.LineEdit2.selectAll()
        self.LineEdit2.copy()

        if self.give_copy_imformation:
            QMessageBox.information(self, u'info', u'The text has been copied to your clipboard!'
                                            '''\n(This message will not appear again!)''')
            self.give_copy_imformation = 0
    

    def set_tag_combobox(self):
        print 'set_tag_combobox'
        self.tag_ComboBox.clear()
        
        if len(self.LineEdit.text()) == 0:
            self.tag_ComboBox.addItems(self.tags)
            return
        tag_index = []
        tag = []
        for i,t in enumerate(self.tags):
            if unicode(self.LineEdit.text()) in t:
                tag_index.append(i)   
        tag = [self.tags[i] for i in tag_index]
        self.tag_ComboBox.addItems(tag)
                
    
    def set_yan_combobox(self):
        print 'set_yan_combobox'
        yan_index = []
        for i,y in enumerate(self.tags):
            if y == unicode(self.tag_ComboBox.currentText()):
                yan_index.append(i)
        yan = []
        for i in yan_index:
            yan += self.yan[i]
        self.yan_ComboBox.clear()
        self.yan_ComboBox.addItems(yan)


    def getData(self):
        try:
            page = open('yan.json')
        except:
            QMessageBox.warning(self , u'error', u"no 'yan.json' file found!")
            QDialog.accept(self)
            exit(1)
            
        data = dict(loads(page.read()))['list']
        tags = [i['tag'] for i in data]
        yan  = [i['yan'] for i in data]
        return tags,yan


def main():
    app = QApplication(argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

