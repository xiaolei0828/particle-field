clear all
close all
clc
d=117;%ֱ��
   nameFig = 1;
%    for indexFig = 1:70;
             %I1 = imread(strcat('C:\Users\dell\Desktop\juji\11',num2str(indexFig),'.jpg'));
  n=input( 'please input number of points n=');
 pic=(imread('G:\yolov5����\��������1\��������yolov5s ����\��Ƶ���\�ֽ�\ԭʼ��Ƶ�ֽ�\1\46.jpg'));
  figure;imshow(pic);
 loc_points=zeros(n,2);

 for i=1:1:n
    
 hold on;  
 [x, y]=ginput(1);%�Լ��޸ĵ�matlabԴ��һС����

 hold on;
 plot(x,y,'r.')%���������б�ǳ���
 
 loc_points(i,1) = x;
 loc_points(i,2) = y;

 str=['  X:' num2str(x') ', Y:' num2str(y')];
text(x,y,cellstr(str))
pic1=pic(:,:,1);
pic2=pic(:,:,2);
pic3=pic(:,:,3);
I21=pic1(y-d/2:y+d/2,x-d/2:x+d/2 );
I22=pic2(y-d/2:y+d/2,x-d/2:x+d/2 );
I23=pic3(y-d/2:y+d/2,x-d/2:x+d/2 );

I2=zeros(d+1,d+1,3);
I2(:,:,1)=I21(:,:);
I2(:,:,2)=I22(:,:);
I2(:,:,3)=I23(:,:);
I2=uint8(I2);
imwrite(I2,(strcat('G:\yolov5����\��������1\��������yolov5s ����\��Ƶ���\�ֽ�\ԭʼ��Ƶ�ֽ�\1\256\46',num2str(nameFig),'.png')),'png');%I2��RGBͼ��I21�ǻҶ�ͼ��
     nameFig = nameFig+1;
end
%    end