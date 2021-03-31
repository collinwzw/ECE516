% % function to read data from pipe-based ECG
% % #Bluepipe(TM)
% 
% f=fopen("ecg_data_EXG_12.COG");
% a=fread(f,'uchar');
% b=reshape(a,16,length(a)/16).';
% channel1 = 256..^3*b(:,4) + 256..^2*b(:,3) + 256..^1*b(:,2) + 256..^0*b(:,1);
% channel2 = 256..^3*b(:,8) + 256..^2*b(:,7) + 256..^1*b(:,6) + 256..^0*b(:,5);
% channel3=channel1-channel2;
% s=215650+0;
% 
% pks = findpeeks(channel3(s:s+range-1))
% range = 3000
% plot(channel3(s:s+range-1),'color',[0 0.3 0],'LineWidth',16);
% set(gca,'xtick',[])
% set(gca,'ytick',[])
% set(gca,'Color','k')
% hold on
% plot(channel3(s:s+range-1),'color',[0 0.5 0],'LineWidth',4);
% plot(channel3(s:s+range-1),'color',[0 0.8 0],'LineWidth',1);
% plot(channel3(s:s+range-1),'color',[0 1 0],'LineWidth',0.25);
% % when it was put on...
% % around noon turned on, put on electrodes around 12:20, jumping jacks around 12:23... arrived at beach 1:30pm.
% % arrived at beach, noticed FLEXVOLT electrodes had fallen off so I put back onto hospital electrodes from feb12
% % the electrodes came off right after swim (while drying off).





% #function to read data from pipe-based ECG
% #Bluepipe(TM)

%the first 260164 data points are garbage.
%that's about 0.087286 of the data at the beginning that's garbage
%only about 91% of the data aferwards...

%then up to sample 1972200 good, but bad after that 
%then good again after 2082000

f=fopen("ecg_data_EXG_14.COG"); % 260165 is the first good data point.
a=fread(f,'uchar');
b=reshape(a,16,length(a)/16).';
channel1 = 256..^3*b(:,4) + 256..^2*b(:,3) + 256..^1*b(:,2) + 256..^0*b(:,1);
channel2 = 256..^3*b(:,8) + 256..^2*b(:,7) + 256..^1*b(:,6) + 256..^0*b(:,5);
channel3=channel1-channel2;s=260165+10000;plot(channel3(s:s+10000-1));
dlmwrite("try.csv",channel3(s:s+10000-1))
