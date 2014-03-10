from PyQt4 import QtCore, QtGui
import sys,csv

class CSVTableModel(QtCore.QAbstractTableModel):


    def __init__(self,data = []  ,headers = [] , parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.__headers = headers
        self.__data = data



    def rowCount(self,parent):
        return len(self.__data)
    

    def columnCount(self,parent):
        return len(self.__headers)


    def data(self,index,role):

        
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]
        
              
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__data[row][column]
            
            return value


    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            column = index.column()
            self.__data[row][column] = str(value.toPyObject())
            
            
            #add last empty row for further entry
            if ((row + 1) == self.rowCount(None) and self.__data[row][0:] != ["" for i in range(self.columnCount(None))] ):
                self.insertLastRow()
    
            self.dataChanged.emit(index, index)
            return True


        else:
            return False



    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
            else:
                return ""


    def getData(self):
        return self.__data[:-1]
        
    def getHeaders(self):
        return self.__headers
        


    def insertRows(self, position, rows, data, parent = QtCore.QModelIndex()):
        
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            if data==[]: 
                self.__data.insert(position + i, ["" for i in self.__headers]) 
            else:
                self.__data.insert(position + i, data[i])        
        
        self.endInsertRows()
          
        return True
        

    
    def insertLastRow(self):
        data = [["" for i in range(self.columnCount(None))]]
        self.insertRows(self.rowCount(None),1,data)
    


    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        pass



    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__data[position]
            self.__data.remove(value)
             
        self.endRemoveRows()
        return True


    def setHeaderData(self,headers):
        self.__headers = headers


    def clearData(self):
        self.removeRows(0,self.rowCount(None))
    


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    tv = QtGui.QTableView()
#    tv.verticalHeader().hide()
    tv.show()
    model = CSVTableModel()


    inputfile = open("t5configfast.csv")
    filecsv = csv.reader(inputfile)
    headers = filecsv.next()
    data = [row for row in filecsv]



    model.insertRows(0,len(data),data)
    model.setHeaderData(headers)
    model.insertLastRow()

    model.insertRows(5,2,[])

    tv.setModel(model)

#    print model.getData()

#    print tv.selectionModel().selection().indexes()



#    model.removeRows(2,3)
#    model.clearData()
#    model.insertLastRow()

    sys.exit(app.exec_())

