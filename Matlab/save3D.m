%%
%²úÉú3DÍ¼Ïñ²¢´æ´¢

%%
numTotal=99;
IU=imread('F:\ExpFor\nd11\29.tif');
IU=double(IU);
IU=IU/max(max(IU));
IU=imresize(IU,0.5);
imshow(IU,[])
[M,N]=size(IU);
dx=4.85E-3*2;
dy=4.85E-3*2;
Mag=50;
lamda=532E-6;
m=1:M;
fy=lamda*(-1/dy/2+1/dy/M*(m-1));
n=1:N;
fx=lamda*(-1/dx/2+1/dx/N*(n-1));
[fxx,fyy]=meshgrid(fx,fy);
HFrnFactor=1*pi/lamda*sqrt(1-(fxx.^2+fyy.^2));
zmin=0.1;
zmax=1;
dz=0.1;
pm2_5t=0;
pm10t=0;
fn2_5=strcat('F:\ExpFor\nd5\pm2_5.txt');
fn10=strcat('F:\ExpFor\nd5\pm10.txt');
pm2_5s=-ones(100,1);
pm10s=-ones(100,1);

X=(1:N)*4.85*2/Mag/1000;
Y=(1:M)*4.85*2/Mag/1000;
[xx,yy]=meshgrid(X,Y);
colormap('jet');
numZ=0;
HFrn=cell(1);
for z=zmin:dz:zmax
    numZ=numZ+1;
    z=Mag.*Mag.*z;
    HF=1i.*z.*HFrnFactor;
    HFrn{numZ}=exp(HF);
end
sensitive=0.05;

for n=0:numTotal
    IU=imread(strcat('F:\ExpFor\nd4\',num2str(n),'.bmp'));
    IU=double(IU);
    IU=imresize(IU,0.5);
    IU=IU/max(max(IU));
%     pm2_5t=pm2_5t+pm2_5;
%     pm10t=pm10t+pm10;
%     pm2_5s(n+1)=pm2_5;
%     pm10s(n+1)=pm10;

    [draw3D2_5,draw3D10,pm2_5,pm10,minIUz,posMinIUz]=...
        focusAutoFastTest(IU,M,N,HFrn,numZ,zmin,dz,sensitive,Mag);
    figure(1)

    draw3D10(draw3D10==zmin-dz)=1.002;
    mesh(xx,yy,draw3D10,draw3D10,'FaceAlpha','1','Marker','.','MarkerSize',12,'lineStyle','none','EdgeAlpha',0)
    axis([0 0.1 0 0.1 0 1])
    text(0.08,0.05,1,strcat('PM10=',num2str(pm10/1000),'ug/L'),'FontSize',10);
    colorbar
    xlabel('x(mm)');
    ylabel('y(mm)');
    zlabel('z(mm)');
    
    saveas(gcf,strcat('F:\Expfor\3d4\',num2str(n),'.tif'),'tif');