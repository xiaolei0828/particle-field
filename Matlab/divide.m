 M =2560;
 N =1922;
nameFig = 1;
for indexFig = 1:30
     IU1 = imread(strcat('G:\ȫϢѪϸ�����\Ѫϸ��ģ��\ԭʼ����\ԭʼ����0\',num2str(indexFig),'.jpg'));
%     IU1 = load(strcat('G:\ȫϢѪϸ�����\Ѫϸ������\defocus\mat\',num2str(indexFig),'.mat'));
%     IU1 = IU1.Phi_FFT 
    %IU = rgb2gray(IU)
    for m =961:50:M
        for n = 1280:50:N
            IU_dev = IU1(m-960:m,n-1279:n);
             imwrite(IU_dev,(strcat('G:\ȫϢѪϸ�����\Ѫϸ��ģ��\ԭʼ����\ԭʼ����0\1\',num2str(nameFig),'.png')),'png');
%             save((strcat('G:\ȫϢѪϸ�����\Ѫϸ������\defocus\mat\256\',num2str(nameFig),'.mat')),'IU_dev')
            nameFig = nameFig+1;
        end
    end
end