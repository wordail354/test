from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

#удолили словарь, надо купить

app = QApplication([])
win = QWidget()

win.setWindowTitle('заметки')
win.move(840,400)
win.resize(500, 400)
bolshazchast = QTextEdit()
spisokzametok = QLabel('Список заметок')
listvidget = QListWidget()
sozdatzametka = QPushButton('Создать заметка')
ydalitzametka = QPushButton('Удалить заметка')
soxranitzametka = QPushButton('Сохранить заметка')
spisoktegov = QLabel('Список тегов')
listtegs = QListWidget()
lineedit = QLineEdit()
lineedit.setPlaceholderText('Введите текст')
dobavitkzametka = QPushButton('Добавить к заметка')
zabratizzameta = QPushButton('Забрать из заметка')
poiskzametkapoteg = QPushButton('Искать заметка по тегу')

vertlina = QVBoxLayout()
vertlina2 = QVBoxLayout()
row = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()

vertlina.addWidget(bolshazchast)
vertlina2.addWidget(spisokzametok)
vertlina2.addWidget(listvidget)
row.addWidget(sozdatzametka)
row.addWidget(ydalitzametka)
row2.addWidget(soxranitzametka)
vertlina2.addLayout(row)
vertlina2.addLayout(row2)
vertlina2.addWidget(spisoktegov)
vertlina2.addWidget(listtegs)
vertlina2.addWidget(lineedit)
row3.addWidget(dobavitkzametka)
row3.addWidget(zabratizzameta)
row4.addWidget(poiskzametkapoteg)
vertlina2.addLayout(row3)
vertlina2.addLayout(row4)

rowxxl = QHBoxLayout()
rowxxl.addLayout(vertlina, stretch=2)
rowxxl.addLayout(vertlina2, stretch=1)
with open('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

listvidget.addItems(notes)

def shownoute():
    kay = listvidget.selectedItems()[0].text()
    bolshazchast.setText(notes[kay]['Текст'])
    listtegs.clear()
    listtegs.addItems(notes[kay]['Теги'])

def add_note():
    note_ima, ok = QInputDialog.getText(win, 'Добавить заметка', 'Название заметка:')
    if ok and note_ima != '':
        notes[note_ima] = {'Текст' : '', 'Теги' : []}
        listvidget.addItem(note_ima)

def del_note():
    if listvidget.selectedItems():
        kay = listvidget.selectedItems()[0].text()
        del notes[kay]
        listtegs.clear()
        bolshazchast.clear()
        listvidget.clear()
        listvidget.addItems(notes)
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('Заметка не выбран')

def save_note():
    if listvidget.selectedItems():
        kay = listvidget.selectedItems()[0].text()
        notes[kay]['Текст'] = bolshazchast.toPlainText()
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('Заметка не выбран')

def add_teg():
    if listvidget.selectedItems():
        kay = listvidget.selectedItems()[0].text()
        tag = lineedit.text()
        if not tag in notes[kay]['Теги']:
            notes[kay]['Теги'].append(tag)
            listtegs.addItem(tag)
            lineedit.clear()
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('заметка не выбран')

def del_teg():
    if listtegs.selectedItems():
        kay = listvidget.selectedItems()[0].text()
        teg = listtegs.selectedItems()[0].text()
        notes[kay]['Теги'].remove(teg)
        listtegs.clear()
        listtegs.addItems(notes[kay]['Теги'])
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False)

def search_tag():
    teg = lineedit.text()
    if poiskzametkapoteg.text() == 'Искать заметка по тегу' and teg:
        notes_filtered = {}
        for note in notes:
            if teg in notes[note]['Теги']:
                notes_filtered[note] = notes[note]
        poiskzametkapoteg.setText('Сбросить поиск')
        listvidget.clear()
        listtegs.clear()
        listvidget.addItems(notes_filtered)
    elif poiskzametkapoteg.text() == 'Сбросить поиск':
        listtegs.clear()
        listvidget.clear()
        lineedit.clear()
        bolshazchast.clear()
        listvidget.addItems(notes)
        poiskzametkapoteg.setText('Искать заметка по тегу')

poiskzametkapoteg.clicked.connect(search_tag)
zabratizzameta.clicked.connect(del_teg)
dobavitkzametka.clicked.connect(add_teg)
soxranitzametka.clicked.connect(save_note)
ydalitzametka.clicked.connect(del_note)
listvidget.itemClicked.connect(shownoute)
sozdatzametka.clicked.connect(add_note)

win.setLayout(rowxxl)
win.show()
app.exec_() 
