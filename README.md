# particle-field
1.图像数据获取及标注 首先对采集的原始数据预处理，这里使用的是精灵标记助手将数据处理为xml文件。下载链接可参考http://www.jinglingbiaozhu.com/ 
2. 图像数据量选取与划分 （1）在YOLOv5的目录下新建一个data的文件夹，在该文件夹下建image，Annotations，Imagesets和labels等四个文件夹。 （2）image文件夹下存储采集到的原始数据 （3）Annotations文件下存储由精灵助手生成的xml文件，此处放置的xml文件必须与image文件夹下存放的原始数据保持一致。 （4）Imagesets存放的是分类和检测的所有数据集文件，包含train.txt用于训练的数据，val.txt用于验证的数据，trainval.txt训练和验证的所有数据，test.txt用于测试的数据。 
3.数据集的分类与运行。 在YOLOv5的根目录下新建makeTxt.py和voc-label.py，其中make.Txt.py主要是用来将数据集自动分为训练集和验证集。 
4.数据已上传到data文件夹，其中包含：浮游生物A、浮游生物B、血细胞、聚苯乙烯微珠的原始显微图像，还包含标注后的xml文件。适应该数据已完成粒子的实时定位追踪，如有需要欢迎下载。
5.Matlab文件夹内包含重建3D空间分布的程序，欢迎广大学者下载使用。 请多多引用Particle field positioning with a commercial microscope based on a developed CNN and the depth-from-defocus method链接https://doi.org/10.1016/j.optlaseng.2022.106989 
在上传过程可能会存在bug，如遇到任何问题欢迎联系handandong@163.com；xiaolei6778@163.com
