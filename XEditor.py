# ­*­coding: utf­8 ­*­
from PyQt4.QtGui import*
from PyQt4.QtCore import*
from pyqterm import TerminalWidget
import pyqterm
from PyQt4.QtCore import Qt, pyqtSignal, SIGNAL
import sys,os
class window(QMainWindow):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        #------------window setting--------------
        self.setWindowTitle('Text Editor')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(400,200,800,800)
        #self.setStyleSheet('background-­color:blue;')
        #-----------------------------------
        
        
        menubar=self.menuBar()
        f=menubar.addMenu('File')
        new=QAction('New',self)
        new.setShortcut('Ctrl+N')
        f.addAction(new)
        new.triggered.connect(self.new_file)
        #-------------------------
        open_f=QAction('Open',self)
        open_f.setShortcut('Ctrl+O')
        f.addAction(open_f)
        open_f.triggered.connect(self.open_file)
        #-------------------------
        save=QAction('Save',self)
        save.setShortcut('Ctrl+S')
        f.addAction(save)
        save.triggered.connect(self.save_file)
        #---------------------------
        close=QAction('Close',self)
        close.setShortcut("Esc")
        close.triggered.connect(self.closeing)
        f.addAction(close)
        edit=menubar.addMenu('Edit')
        font=QAction('Font',self)
        edit.addAction(font)
        font.triggered.connect(self.font)
        #--------------------------------------
        indent=QAction("Indent",self)
        indent.setShortcut('Tab')
        indent.triggered.connect(self.identation)
        dedent=QAction('Dedentation',self)
        dedent.setShortcut('Ctrl+Tab')
        dedent.triggered.connect(self.dedentation)
        #-------------------------------------------
        toolbar=self.addToolBar('')
        run=QAction('Run',self)
        color=QAction('Color',self)
        help=QAction('help',self)
        toolbar.addAction(run)
        toolbar.addAction(color)
        toolbar.addAction(help)
        run.triggered.connect(self.running)
        
        #-------------------------
        self.dock=QDockWidget('Itool',self)
        self.dock.setGeometry(2,50,200,530)
        self.listbox=QListWidget()
        self.listbox.setStyleSheet('background-color:black;'
                                   'color:green;')
        self.dock.setWidget(self.listbox)
        self.dock.setFeatures(QDockWidget.DockWidgetClosable)
        #-----------------------------------
        self.tab=QTabWidget(self)
    
        self.tab.setGeometry(210,50,560,530)
        self.tabs=QWidget()
        self.tabs.setStyleSheet('background-color:darkgray;')
        self.tab.addTab(self.tabs,'New')
        self.tab.setMovable(True)
        self.tab.setTabsClosable(True)
        self.tab.tabBar().tabCloseRequested[int].connect(self.tabcl)

        
        self.textedit=QTextEdit(self.tabs)
        self.textedit.resize(560,480)
        #self.textedit.setStyleSheet("color:white;")
        self.textedit.cursorPositionChanged.connect(self.cursorposition)
        self.highlighter = Highlighter(self.textedit.document())
        #---------------------------------------

        self.term=TerminalWidget(self)
        self.term.setGeometry(210,590,560,180)
        self.term.zoom_out()
        self.term.zoom_out()        
        self.term.show()
    
        self.show()
        
    def new_file(self):
        self.tabs=QWidget()
        self.textedit=QTextEdit(self.tabs)
        self.textedit.resize(560,500)
        self.textedit.setStyleSheet("color:white;")
        self.tabs.setStyleSheet('background-color:black;')
        self.tab.addTab(self.tabs,'untitled')
        
    def open_file(self):
        try:
            self.filename = QFileDialog.getOpenFileName(self,'Open file')
            i = open(self.filename,'r')
            with i:
                f=i.read()
                self.textedit.setText(f)
                self.listbox.addItem(str(i.name))
            
            
        
        except IOError:
            pass
        except UnicodeDecodeError:
            pass
   
            
            
            
            
            
    def save_file(self):
            self.name=QFileDialog.getSaveFileName(self,'Open file','/home','Save File (*.py)')
            file=open(self.name,'w')
            text=self.textedit.toPlainText()
            file.write(text)
            file.close
            
    def tabcl(self,index):
        self.tab.removeTab(index)
            
    def running(self):
        try:
            import os
            os.system("xterm -hold -e 'python {}; write'".format(str(self.filename)))
        except AttributeError:

            self.listbox.addItem('choose file then click run')
            pass
    def cursorposition(self):
        
        cursor = self.textedit.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusBar().showMessage("Line: {} | Column: {}".format(line,col))
    def font(self):
        ok,font=QFontDialog.getFont()
        if font:
            self.textedit.setFont(ok)
    def identation(self):
        cursor = self.textedit.textCursor()

        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.selectionEnd())
            diff = cursor.blockNumber() - temp
            for n in range(diff + 1):
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.insertText("\t")
                cursor.movePosition(QtGui.QTextCursor.Up)
        else:
            cursor.insertText('\t')
    def dedentation(self):
        cursor = self.textedit.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.selectionEnd())
            diff = cursor.blockNumber() - temp
            for n in range(diff + 1):
                self.handleDedent(cursor)
                cursor.movePosition(QTextCursor.Up)
        else:
            self.handleDedent(cursor)
    def handleDedent(self,cursor):
        cursor.movePosition(QTextCursor.StartOfLine)
        line = cursor.block().text()
        if line.startswith("\t"):
            cursor.deleteChar()
        else:
             for char in line[:8]:
                 if char != " ":
                     break
                 cursor.deleteChar()
    def closeing(self):
        self.close()

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\".*\""),
                quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,startIndex + commentLength);
if __name__ == '__main__':
    app = QApplication([])
    gui = window()
    app.exec_()
