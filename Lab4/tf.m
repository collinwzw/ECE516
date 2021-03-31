% sliding window FFT with hanning + appropriate overlap   Steve Mann, 1990oct22
%
% (no longer subtracts mean from data)
%
% Y = tf(x);      % default is to make as close to square array as possible
%                 % with an overlap of 1/2
%
% Y = tf(x,M);    % does M point ffts for each line;  defaults to square M=N
%
% Y = tf(x,M,N)   % creates M by N matrix doing correct amount of overlap
%                 % (pos or neg as needed) to use all the data
%
% Y = tf(x,256,256,2) % doubles the length of each fft by padding
% Y = tf(x,256,256,4) % generates a 1024 by 256 image by padding each col. fft
%
% M is length of each FFT; N is number of ffts to be done
%
% size of returned matrix is  (M*padratio by N) 

function TF = dummy(x,M,N,padratio)

if nargin < 4
  padratio = 1; % defaults to no extra padding
end%if

pad = [];
if nargin ==4
  pad = zeros(M*(padratio-1),1);
end%if

len = length(x);
if nargin == 2
  N = M;   % default to square
end%if

if nargin == 1
  disp('selecting M and N to get a matrix close to being square')
  disp('and have an overlap of 1/2')
  default_overlap = 1/2;
  M = round(sqrt(len/default_overlap));  % eg sqrt(twice len)
  N = M;   % do however many ffts necessary for overlap of 1/2
end%if

%%%%%%%%%%%%%%%%%%%%%% DISP
disp(sprintf('number of FFTs to be done = %g; length of each = %g padded to %g',N,M,M*padratio))

%%%%%%disp('subtracting mean')
%%%%%%x = x(:) - mean(x(:));
%%%%%%disp('subtracted mean')

TF = NaN*ones(M+length(pad),N);  % initialise tf so malloc not reapeated

window = hanning(M); % M data points are windowed first then padded if desired
for n=1:N
  space = (len-M*N)/(N-1); % space left between each fft (space usually < 0)
  % space between each fft is preferably less than zero to give overlap
  lo_index = (n-1)*M + (n-1)*space+1;  % number of Ms and spaces so far
  lo_index = round(lo_index); % save warnings in newer versions of matlab
  hi_index = n*M     + (n-1)*space;    % = lo_index + M-1
  hi_index = round(hi_index); % save warnings in newer versions of matlab
%%%%%%%%%%%%%%%%%%%%%%  DISP
  disp(sprintf('col %g (from sample %g to sample %g)',n,lo_index,hi_index))
%  coldat = [pad ; x(lo_index:hi_index).*hanning(hi_index-lo_index+1)];
  coldat = [pad ; x(lo_index:hi_index).*window]; % time domain dat. in each col.
  TF(:,n) = 1/sqrt(M)*fftshift(fft(coldat));
  % the 1/sqrt(M) is to satisfy plancheral: ie if time series A is twice as
  % long as time series B, its power spectrum will have twice the area under it
  % remember concatenation with itself doubles area under PDF or PWR spec
  % note hanning has area=1/2 and power/len = .375, so it wont affect normalis
  % if FFT padded, it needs to be scaled only by portion contributing energy
end%for

TF = flipud(TF);  % want high freq. at lowest m indices (top)
