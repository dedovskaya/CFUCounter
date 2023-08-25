from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QHBoxLayout, QLabel, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QIcon
import PyQt5.QtCore as QtCore
import sys
import os
import re
import pandas as pd
import datetime
import warnings
warnings.filterwarnings("ignore", message=r"Passing", category=FutureWarning)
from count_sectors import *

# Paths
model_path = 'agar_cfg20221010T2320/mask_rcnn_agar_cfg_0004.h5'
data_path = 'agar2'

# MRCNN imports
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
# from mrcnn.config import Config
from mrcnn.model import MaskRCNN

# Agar imports
from agarConfig import PredictionConfig
rcnn = MaskRCNN(mode='inference', model_dir='./', config=PredictionConfig())
rcnn.load_weights(model_path, by_name=True)


class Ui(QtWidgets.QWidget):
   def __init__(self):
      super(Ui, self).__init__()
      uic.loadUi('gui_agarcnn.ui', self)
      with open("style.qss") as f: 
         f = f.read()
         self.setStyleSheet(f)
      # Set the window title
      self.setWindowTitle('CFUCounter')
      # Set the window icon
      self.setWindowIcon(QIcon('icon.png'))
      # self.splitter.setOpaqueResize(False)
      self.bopenfile.clicked.connect(lambda: self.openFile())
      self.bopenfolder.clicked.connect(lambda: self.openFolder())
      self.bnext.clicked.connect(lambda: self.showNext())
      self.bprevious.clicked.connect(lambda: self.showPrevious())
      self.bdetect.clicked.connect(lambda: self.detect())
      self.bexportimg.clicked.connect(lambda: self.exportImg())
      self.bexportresults.clicked.connect(lambda: self.exportResults())
      self.thumbnailframe_layout = QHBoxLayout(self.thumbnailframe)
      self.thumbnailframe.setLayout(self.thumbnailframe_layout)
      self.scene = QGraphicsScene(self.graphicsView)
      self.graphicsView.setScene(self.scene)
      self.bdetectall.clicked.connect(lambda: self.detectAll())
      self.bguide.clicked.connect(lambda: self.guideOpen())
      self.progress_val = 0
      # Preferences
      self.numsamples.valueChanged.connect(lambda: self.editConfig())
      self.detconfidence.valueChanged.connect(lambda: self.editConfig())

      # self.progressBar
      # Tooltips
      self.bopenfile.setToolTip('Upload one file.') 
      self.bopenfolder.setToolTip('Upload files from folder.') 
      self.numsamples.setToolTip('Maximum number of final detections.') 
      self.detconfidence.setToolTip('Minimum probability value to accept a detected instance. ROIs below this threshold are skipped') 
      self.bexportimg.setToolTip('Export displayed image.') 
      self.bexportresults.setToolTip('Export .csv file with detection results.') 

      self.show()

      # Data for export
      self.data = {
      'filename' : [],
      'Number of colonies' : [],
      'bboxes': [],
      'conf_numsamples' : [],
      'conf_det_confidence': [],
      'sec0' : [],
      'sec1' : [],
      'sec2' : [],
      'sec3' : [],
      'sec4' : []
      }
      # Table
      self.rows = 1
      self.currentFile = 0

      self.textoutputlabel.setText('Log')

   def openFile(self):
      fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)" )
      print(fileName)
      self.currentFile = fileName
      self.showImg(fileName)

   def showImg(self, fileName):
      self.scene.clear()
      pix = QPixmap(fileName)
      item = QGraphicsPixmapItem(pix)
      self.scene.addItem(item)
      self.graphicsView.fitInView(item, QtCore.Qt.KeepAspectRatio)

      
   def openFolder(self):
      dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'F:\\', QtWidgets.QFileDialog.ShowDirsOnly)
      self.files = [f for f in os.listdir(dir_) if re.match(r'.*\.jpg', f)]
      self.files = [os.path.join(dir_, f) for f in self.files]

      if len(self.files) > 0:
         self.showImg(self.files[0])
         self.currentFile = self.files[0]
         self.currentIndex = 0
      for file in self.files:
         label = QLabel(self.thumbnailframe)
         print(os.path.join(dir_,file))
         label.setFixedSize(100,100)
         label.setPixmap(QPixmap(file).scaled(100,100) )
         self.thumbnailframe_layout.addWidget(label)
         
      print(self.files)

   def showNext(self):
      self.currentIndex = min(self.currentIndex + 1, len(self.files) -1 )
      self.currentFile = self.files[self.currentIndex]
      self.showImg(self.currentFile)

   def showPrevious(self):
      self.currentIndex = max(self.currentIndex - 1,0)
      self.currentFile = self.files[self.currentIndex]
      self.showImg(self.currentFile)
      
   def detect(self):
      if self.currentFile == 0:
         output_str = "Please, upload a file."
         self.updateText(output_str)
         return

      self.progressBar.setFormat('Loading...')
      self.progressBar.setValue(10)
      rcnn = MaskRCNN(mode='inference', model_dir='./', config=PredictionConfig())
      rcnn.load_weights(model_path, by_name=True)
      #MRCNN code
      img = load_img(self.currentFile)
      img = img_to_array(img)
      # make prediction
      self.results = rcnn.detect([img], verbose=0)
      num_colonies = len(self.results[0]['rois'])
      img_name = os.path.split(self.currentFile)[1]
      output_str = img_name + ' number of colonies: ' + str(num_colonies)
      self.updateText(output_str)

      # Count colonies sectorwise
      sectorwise = sectCount(bboxes=self.results[0]['rois'], img=img)
      print(sectorwise)
      self.data['sec0'].append(sectorwise[0])
      self.data['sec1'].append(sectorwise[1])
      self.data['sec2'].append(sectorwise[2])
      self.data['sec3'].append(sectorwise[3])
      self.data['sec4'].append(sectorwise[4])

      # Draw boxes
      pen = QPen(QColor(255,0,0))
      pen.setWidth(10)
      for box in self.results[0]['rois']:
         y1, x1, y2, x2 = box
          # calculate width and height of the box
         width, height = x2 - x1, y2 - y1
         box = QGraphicsRectItem(x1, y1, width, height)
         box.setPen(pen)
         self.scene.addItem(box)

      # Update data dictionary
      self.data['filename'].append(os.path.split(self.currentFile)[1])
      self.data['Number of colonies'].append(num_colonies)
      self.data['bboxes'].append(self.results[0]['rois'])
      self.data['conf_numsamples'].append(self.numsamples.value())
      self.data['conf_det_confidence'].append(self.detconfidence.value())
      self.progressBar.setFormat('Done')
      self.progressBar.setValue(100)
      # Update table
      self.updateTable()

   def updateTable(self):
      self.rows = len(self.data["filename"])
      self.tableWidget.setRowCount(self.rows)
      for i in range(len(self.data["filename"])):
         self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.data["filename"][i])))
         self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.data['Number of colonies'][i])))
         self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.data['bboxes'][i])))

   def detectAll(self):
      if self.currentFile == 0:
         output_str = "Please, upload a file."
         self.updateText(output_str)
         return
      # setting text 
      self.progressBar.setFormat('Loading...')
      self.progressBar.setValue(0)
      rcnn = MaskRCNN(mode='inference', model_dir='./', config=PredictionConfig())
      rcnn.load_weights(model_path, by_name=True)
      prog_step = 100/(len(self.files))
      for file in self.files:
         #MRCNN code
         self.scene.clear()
         self.showImg(file)

         img = load_img(file)
         img = img_to_array(img)
         # make prediction
         self.results = rcnn.detect([img], verbose=0)
         num_colonies = len(self.results[0]['rois'])
         output_str = str(self.currentFile) + ' number of colonies: ' + str(num_colonies)
         self.updateText(output_str)

         # Count colonies sectorwise
         sectorwise = sectCount(bboxes=self.results[0]['rois'], img=img)
         print(sectorwise)
         self.data['sec0'].append(sectorwise[0])
         self.data['sec1'].append(sectorwise[1])
         self.data['sec2'].append(sectorwise[2])
         self.data['sec3'].append(sectorwise[3])
         self.data['sec4'].append(sectorwise[4])

         # Draw boxes
         pen = QPen(QColor(255,0,0))
         pen.setWidth(10)
         for box in self.results[0]['rois']:
            y1, x1, y2, x2 = box
            # calculate width and height of the box
            width, height = x2 - x1, y2 - y1
            box = QGraphicsRectItem(x1, y1, width, height)
            box.setPen(pen)
            self.scene.addItem(box)

         # Update data dictionary
         self.data['filename'].append(os.path.split(file)[1])
         self.data['Number of colonies'].append(num_colonies)
         self.data['bboxes'].append(self.results[0]['rois'])
         self.data['conf_numsamples'].append(self.numsamples.value())
         self.data['conf_det_confidence'].append(self.detconfidence.value())
         self.progressBar.setValue(self.progress_val + prog_step)
      self.progressBar.setFormat('Done')
      self.progressBar.setValue(100)

      # Update table
      self.updateTable()

   def exportResults(self):
      df = pd.DataFrame(self.data)
      now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      name = "detection_results_" + now + ".csv"
      df.to_csv(name, index=False, header=True)
      output_str = 'Detection results saved to root folder.'
      self.updateText(output_str)

   def exportImg(self):
      if self.currentFile == 0:
         output_str = "Please, upload a file."
         self.updateText(output_str)
         return

      image = QImage(200,200, QImage.Format_ARGB32);   
      painter = QPainter(image);
      self.scene.render(painter);
      painter.end()
      img_name = os.path.split(self.currentFile)[1][0:-4]
      new_img_name = img_name + '_bboxes.png'
      image.save(new_img_name);
      output_str = "Image saved to " + new_img_name
      self.updateText(output_str)
   
   def editConfig(self):
      PredictionConfig.DETECTION_MAX_INSTANCES = self.numsamples.value()
      PredictionConfig.DETECTION_MIN_CONFIDENCE = self.detconfidence.value()

   def guideOpen(self):
      import webbrowser
      webbrowser.open('file://' + os.path.realpath("guide.html"))

   def updateText(self, output_str):
      text = self.textoutputlabel.text()
      t = str(datetime.datetime.now())[0:-7] + ": "
      self.textoutputlabel.setText(t + output_str + '\n' + text)
      

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()