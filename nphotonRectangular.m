%--------------------------------------------------------------------------
%                            DESCRIPTION: 
%--------------------------------------------------------------------------
% This program uses fourier transform to convolve and anti fourier
% transform to recover the data. This allowed us to calculate pile up in
% O(NlogN) time for rectangular shaped pulses. This can calculate pile up
% for arbitary count rate and arbitary spectrum but can not predict pile up
% of anything but rectangular pulse shapes.
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% PARAMETERS
%--------------------------------------------------------------------------
Emin = 0; % Minimum Energy
Emax = 6; % Maximum Energy
Total_bins = 10000; % Number of bins in Energy Array


count_rate = 1; % count rate of the spectrum
tf = 1;% dead time of pulses
utf=count_rate*tf; % overlap probablity 

bar = 1e-2; % The lowest value shown in graph
%--------------------------------------------------------------------------
% INPUT SPECTRUM
%--------------------------------------------------------------------------
E = linspace(Emin,Emax,Total_bins); % Energy Array
dE = E(2)-E(1); % increment in energy between bins

input_spectrum = exp(-(E-1).^2/0.1^2); % the function of the spectrum

% normalized probablity distribution for input spectrum
integral_input_spectrum=sum(input_spectrum)*dE;
P = input_spectrum/integral_input_spectrum; 


%--------------------------------------------------------------------------
% PILEUP, O(NlogN) time
%--------------------------------------------------------------------------
Pf = fft(P)*dE; % fourier transform
F = Pf.* exp(utf*(Pf-1)); % the convolution formula in fourier space
output_spectrum = ifft(F); %reverse fourier transform for piled-up spectrum

% normalized probablity distribution for input spectrum
Pn=output_spectrum/(sum(output_spectrum)*dE); 

%--------------------------------------------------------------------------
% PLOT
%--------------------------------------------------------------------------
figure 
semilogy(E,max(P,bar),'LineWidth',2);
hold on
semilogy(E,max(Pn,bar),'LineWidth',2);
hold off
title('Fourier PPU for Rectangular pulses with dead time = ' ...
    +string(tf)+' and count rate = '+string(count_rate));
ylabel('Probablity Distribution', 'FontSize',14);
xlabel('Energy',  'FontSize',14);
grid on;
grid minor;
lgd=legend('raw input spectrum','piled up output spectrum');
lgd.FontSize = 14;