clc
close all
clear
x=[133 128 120 110 101 90 78 72 62 50 41];
y=[70 65 53 56 61 57 63 70 71 75 90];
z=[20 20 20 20 80 60 60 60 60 60 40]; 
sz=65;
c=linspace(0,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z);
axis([0 150 0 100 0 100]); 
  set(gca,'XTick',(0:75:150));
  set(gca,'YTick',(0:50:100));
  set(gca,'ZTick',(0:50:100));
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[110 107.6 104 102 99.8 96 93 90.4 88.6 86.5];
y=[82.2 83 83.6 85.7 86.1 87.3 88.7 90.3 90.7 96.9];
z=[0 0 0 0 0 0 0 0 0 0];
sz=65;
c=linspace(0,4.5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
colorbar;
grid on; 
 x=[93.2 76 56 38.8 22];
 y=[63.6 70.3 78.4 84.7 91.7];
 z=[-80 -80 -80 -80 -80];
sz=65;
c=linspace(0,2,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[139.5 126.2 110.7 97.4 84.4 69.3];
y=[131 137 143 147.9 154.5 159.4];
z=[-60 -60 -60 -60 -60 -60];
sz=65;
c=linspace(0,2.5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[78.5 72.8 66.5 60.9 55 49.3 42 37.8 31.4 26.5 22];
y=[79.1 81.5 83.5 86.1 89 90.7 94.2 95.6 98 99.4 101.5];
z=[-20 -20 -20 -20 -20 -20 -20 -20 -20 -20 -20];
sz=65;
c=linspace(0,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[186.8 165.8 141.3 117.7 97.8 76.3 58.8 39.2]; 
y=[34.5 42.9 52.8 61.2 68.2 76.6 82.2 90.3];
z=[-80 -80 -80 -80 -80 -80 -80 -80];
sz=65;
c=linspace(1.5,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[173.2 166.5 156.7 149 141.6 132.9 123.7 117 109 94.3 95.7];
y=[62.2 65.7 69.6 72.8 76.3 79.8 83.3 86.4 89.3 91.7 94.5];
z=[-20 -20 -20 -20 -20 -20 -20 -20 -20 -20 -20];
sz=65;
c=linspace(0,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on; 
x=[132.5 111.4 88.3 67.9 48.3 25.8 4.4];
y=[99.4 107.5 117 125.4 132.4 140.5 149.6];
z=[-80 -80 -80 -80 -80 -80 -80];
sz=65;
c=linspace(0,3,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[215.7 197.1 179.5 165.8 150 137.1 122];
y=[122.5 130 137.7 142.9 150 155.6 162];
z=[-60 -60 -60 -60 -60 -60 -60];
sz=65;
c=linspace(2,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[108 93.9 77.4 62.7];
y=[141.5 147.9 154.2 160];
z=[-60 -60 -60 -60];
sz=65;
c=linspace(0,1.5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[204.1 190.7 176.7 164.4 151.8];
y=[77.3 82.9 88.2 92.8 98.7];
z=[-60 -60 -60 -60 -60];
sz=65;
c=linspace(3,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on; 
x=[207.6 192.9 180.6 168 154 140.2 128.3];
y=[129.3 135.2 140.5 146.1 151.7 160 161.9];
z=[-60 -60 -60 -60 -60 -60 -60];
sz=65;
c=linspace(0.5,3.5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[214];
y=[26];
z=[0];
sz=65;
c=linspace(0,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;
x=[23];
y=[33.5];
z=[0];
sz=65;
c=linspace(0,5,length(x));
scatter3(x,y,z,sz,c,'filled');hold on
plot3(x,y,z,'-');
map=colormap(flipud(parula));
h=colorbar;
set(get(h,'Title'),'string','tims/s');
set(h,'FontSize',24);  % 设置字体大小
grid on;