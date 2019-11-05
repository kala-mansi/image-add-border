import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QMessageBox)
from PIL import Image
from PIL import ImageDraw
import os
import glob

#path = "173.jpg"

def img_add_rectangle(path):
    img = Image.open(path)
    rgba_image = img.convert('RGBA')
    overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(overlay)
    image_draw.rectangle((0, 0, img.width - 1, img.height - 1), fill=None, outline="red")
    image_draw.rectangle((1, 1, img.width - 2, img.height - 2), fill=None, outline="yellow")
    image_merge = Image.alpha_composite(rgba_image, overlay)
    image_merge.save(path)
    # image_merge.save("out.png")


class MyForm(QDialog):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setWindowTitle("图片加边框(请将图片文件拖入窗口)")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        # print(e.mimeData().formats())
        if e.mimeData().hasFormat('text/uri-list'):
            # print(e.mimeData().text())
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        info = str(e.mimeData().text())
        print(info)
        if info.lower().startswith("file://"):
            # print(e.mimeData().text())
            # print(info)
            if info.count("\n") > 0:  # 多行
                lines = info.split("\n")
                for line in lines:
                    fullpath = line[8:]
                    self.modify_one_file(fullpath)
            else:  # 单行
                fullpath = info[8:]
                if os.path.isdir(fullpath):
                    # QMessageBox.information(self, "提示: 这是一个目录", "这是一个目录")
                    for fname in glob.iglob("{}/*".format(fullpath)):
                        # print(fname)
                        self.modify_one_file(fname)
                else:
                    self.modify_one_file(fullpath)
            QMessageBox.information(self, "提示: 加边框完成", info)

    def modify_one_file(self, fullpath):
        # print(fullpath)
        if ".jpg" in fullpath.lower() or ".png" in fullpath.lower():
            img_add_rectangle(fullpath.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
form = MyForm()
form.show()
app.exec_()
