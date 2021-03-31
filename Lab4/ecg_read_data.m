%read data from pipe-based ECG
%Wednesday 2021mar10
%EXG_15:

%Data recording started at 1:37:01pm and ended at 3:38:03pm, i.e. data duration is 2h, 1m, and 2s.
%7262 seconds

%octave:37> 1959936/7262 % 1959936 samples in 2h, 1m, and 2sec. =  269.889286697879 samples/sec

%octave:32> s=66019;plot(e1(s:s+199999)) % bad
%octave:33> s=66020;plot(e1(s:s+199999)) % good
%the first 66019 data points of channel 1 are garbage.
%the first 70389 data points of channel 2 are garbage (less than 3.6% of the data is bad)

%thus there are 1889547 samples of good data.
%the swim was around the millionth sample of the good data?

f=fopen("ecg_data_EXG_15.COG");
a=fread(f,'uchar');
b=reshape(a,16,length(a)/16).';
%channel1 and channel2:
c1 = 256..^3*b(:,4) + 256..^2*b(:,3) + 256..^1*b(:,2) + 256..^0*b(:,1);
c2 = 256..^3*b(:,8) + 256..^2*b(:,7) + 256..^1*b(:,6) + 256..^0*b(:,5);
e = c1 - c2;

%remove the first 66019 data points (garbage at beginning before connecting to body)
s=70390; c1=c1(s:length(c1)); c2=c2(s:length(c2));
s=245001;
% s = s + 1600000
e = c1 - c2;
e = e(s:s+9999);
% a = reshape(e,[1 , size(e)]);
% SampFreq = 270;
% hlength=100;
% time=(1:1999)/SampFreq;
% fre=1/700:2/700:500;
% 
% %N=7.
% N=7;
% [tfr,tt,ff] = GLCT((a)',N,SampFreq,hlength);
% figure
% imagesc(time,fre,abs(tfr).^2);
% axis xy
% ylabel('Freq / Hz');
% xlabel('Time / Sec')
% title('GLCT,N=7');
% 
% %Reconstruction of Signal
% [m, n] = size(a);
% [v, I] = max(abs(tfr),[],1);
% for j=1:n
% rsig(j)=real(tfr(I(j),j));
% end
% 
% hlength=hlength+1-rem(hlength,2);
% h = tftb_window(hlength);
% h=h/norm(h);
% 
% rsig=rsig/(sum(h)/2);
% %'rsig' is the reconstructed signal form GLCT, by ridge reconstruction method.
% %'cor' is the correlation coffecient between original signal and recovered signal.
% cor=corr(a',rsig');
% %plot the original signal and recovered signal.
% figure
% plot(a);hold on;
% plot(rsig,'r');
% title('Original signal (blue). Recovered signal (red).');

% plot(e);
% figure;
% % TF = tf(e);
% TF = tf(e,2000,1000);
% % imagesc(log(abs(TF)))
% %Ec = TF(1:size(TF)/2,:);
% imagesc(log(abs(TF(750:1000,:))+1))

% P=9; % number of plots: just over 1.9 million samples of good data; 200000 * 9
% for p = 1:P
%  subplot(P,1,p)
%  s = (p-1)* 200000 + 1;
%  plot(e(s:s+199999));
% end%for
CFF=ff(e);
plot(log(abs(CFF)))
figure;
imagesc(log(abs(CFF))+1000)