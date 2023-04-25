% clc;
% close all;
% clear;
% x1=[490 514 540 561 593 602 613 611 613 615 628 637 638 650 654 677 686 701 704 727 720 781 754];
% y1=[473 468 473 463 457 464 467 470 478 483 485 491 491 490 490 494 505 505 512 516 531 550 546]; 
% z1=[60 40 20 40 0 0 40 0 0 0 0 0 0 0 0 0 0 40 40 40 40 40 40];  
%  for n=1:23,
%   x=(x1(n));
%   y=(y1(n));
%   z=(z1(n));
%    figure(n);
%   c=linspace(0,12,length(x));
%   h=scatter3(x,y,z,c,'.','MarkerEdgeColor','k');hold on; %'filled'
%   plot3(x,y,z,'.K','Markersize',30);
%   axis([400 800 450 550 0 100]); 
%   set(gca,'XTick',(400:600:800));
%   set(gca,'YTick',(450:500:550));
%   set(gca,'ZTick',(-20:30:80));
%   grid on;
%   saveas(h,strcat('C:\Users\dell\Desktop\沙雕\',num2str(n),'.png'));
%  end
 
%  同一个位置加时间
img = imread('C:\Users\dell\Desktop\1\27.jpg');
imshow(img);
text(40,40,'t=11s','Fontsize',20,'Color','w' );
% imwrite(img,'C:\Users\dell\Desktop\1\2\1.png');
