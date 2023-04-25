import os
from xml.dom import minidom


class VOC_Sample_Generator:

    def __init__(self):
        self.dom = minidom.Document()
        self.root_node = self.dom.createElement('annotation')
        self.folder_node = self.dom.createElement('folder')
        text = self.dom.createTextNode('-40')
        self.folder_node.appendChild(text)
        self.filename_node = self.dom.createElement('filename')
        self.path_node = self.dom.createElement('path')
        self.source_node = self.dom.createElement('source')
        self.size_node = self.dom.createElement('size')
        self.database_node = self.dom.createElement('database')
        self.width_node = self.dom.createElement('width')
        self.height_node = self.dom.createElement('height')
        self.depth_node = self.dom.createElement('depth')
        self.segmented_node = self.dom.createElement('segmented')

        self.root_node.appendChild(self.folder_node)
        self.root_node.appendChild(self.filename_node)
        self.root_node.appendChild(self.path_node)
        self.root_node.appendChild(self.source_node)
        self.root_node.appendChild(self.size_node)
        self.source_node.appendChild(self.database_node)
        self.size_node.appendChild(self.width_node)
        self.size_node.appendChild(self.height_node)
        self.size_node.appendChild(self.depth_node)
        self.root_node.appendChild(self.segmented_node)

        # self.dom.createTextNode(str(xmin))

    def add_text(self, filename, path, database, segmented):
        text = self.dom.createTextNode(filename)
        self.filename_node.appendChild(text)
        text = self.dom.createTextNode(path)
        self.path_node.appendChild(text)
        text = self.dom.createTextNode(database)
        self.database_node.appendChild(text)
        text = self.dom.createTextNode(str(segmented))
        self.segmented_node.appendChild(text)

    # def add_class(self, class_name):
    #     text = self.dom.createTextNode(class_name)
    #     name_node = self.dom.createElement('name')
    #     name_node.appendChild(text)
    #     self.object_node.appendChild(name_node)

    def add_size(self, width, height, depth):
        text = self.dom.createTextNode(str(width))
        self.width_node.appendChild(text)

        text = self.dom.createTextNode(str(height))
        self.height_node.appendChild(text)

        text = self.dom.createTextNode(str(depth))
        self.depth_node.appendChild(text)


    def add_object(self, name, pose, truncated, difficult,xmin, ymin, xmax, ymax):
        text = self.dom.createTextNode(str(xmin))
        xmin_node = self.dom.createElement('xmin')
        xmin_node.appendChild(text)

        text = self.dom.createTextNode(str(ymin))
        ymin_node = self.dom.createElement('ymin')
        ymin_node.appendChild(text)

        text = self.dom.createTextNode(str(xmax))
        xmax_node = self.dom.createElement('xmax')
        xmax_node.appendChild(text)

        text = self.dom.createTextNode(str(ymax))
        ymax_node = self.dom.createElement('ymax')
        ymax_node.appendChild(text)

        bndbox_node = self.dom.createElement('bndbox')
        name_node = self.dom.createElement('name')
        pose_node = self.dom.createElement('pose')
        truncated_node = self.dom.createElement('truncated')
        difficult_node = self.dom.createElement('difficult')
        object_node = self.dom.createElement('object')
        object_node.appendChild(name_node)
        object_node.appendChild(pose_node)
        object_node.appendChild(truncated_node)
        object_node.appendChild(difficult_node)
        object_node.appendChild(bndbox_node)


        bndbox_node.appendChild(xmin_node)
        bndbox_node.appendChild(ymin_node)
        bndbox_node.appendChild(xmax_node)
        bndbox_node.appendChild(ymax_node)
        text = self.dom.createTextNode(str(name))
        name_node.appendChild(text)
        text = self.dom.createTextNode(str(pose))
        pose_node.appendChild(text)
        text = self.dom.createTextNode(str(truncated))
        truncated_node.appendChild(text)
        text = self.dom.createTextNode(str(difficult))
        difficult_node.appendChild(text)
        self.root_node.appendChild(object_node)


    def build(self, path):
        self.dom.appendChild(self.root_node)
        with open(path, 'w') as f:
            self.dom.writexml(f, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        f.close()

# 测试
if __name__ == "__main__":
    # 打开txt文件路径
    line = 0
    path = './DaTa'
    for list in os.listdir(path):

        print(list)
        voc = VOC_Sample_Generator()
        voc.add_text(filename=str(line)+'.jpg', path='/home/w/zxl/-40/'+str(line)+'.jpg', database='Unknown', segmented=0)
        voc.add_size(1024, 712, 3)

        with open(path+ '/'+list, encoding='utf-8') as file:
            for row in file.readlines():
                # content = file.readline()
                s = row.split()
                # //输入xmax和ymax的值
                voc.add_object(name='depth:'+s[2], pose='Unspecified', truncated=0, difficult=0,\
                               xmax=float(s[0])-0.1, xmin=float(s[0])+0.1, ymax=float(s[1])-0.1, ymin=float(s[1])+0.1)
        voc.build('./test' + list[0:-4] + '.xml')
        line+=1
