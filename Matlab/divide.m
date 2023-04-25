 M =2560;
 N =1922;
nameFig = 1;
for indexFig = 1:30
     IU1 = imread(strcat('G:\全息血细胞相关\血细胞模型\原始数据\原始数据0\',num2str(indexFig),'.jpg'));
%     IU1 = load(strcat('G:\全息血细胞相关\血细胞测试\defocus\mat\',num2str(indexFig),'.mat'));
%     IU1 = IU1.Phi_FFT 
    %IU = rgb2gray(IU)
    for m =961:50:M
        for n = 1280:50:N
            IU_dev = IU1(m-960:m,n-1279:n);
             imwrite(IU_dev,(strcat('G:\全息血细胞相关\血细胞模型\原始数据\原始数据0\1\',num2str(nameFig),'.png')),'png');
%             save((strcat('G:\全息血细胞相关\血细胞测试\defocus\mat\256\',num2str(nameFig),'.mat')),'IU_dev')
            nameFig = nameFig+1;
        end
    end
end