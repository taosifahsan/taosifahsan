%--------------------------------------------------------------------------
%                           DESCRIPTION: 
%--------------------------------------------------------------------------
% This program uses dynamic programming to calculate necessary integrations
% and predict pile up for trapezoidal pulses with arbitary triangularity
% and arbitary spectrum. Using dynamic programming brought down the time of
% integrations from O(N^3) to O(N^2). This program fails to work correctly
% for high count rates. 
%--------------------------------------------------------------------------


%--------------------------------------------------------------------------
% PARAMETERS
%--------------------------------------------------------------------------
% specified parameters
count_rate = 0.1; % this is pulse per unit time
tr = 1.0; % rise time
tf = 0.0; % flat top time
E_min = 0.001; % Minimum energy of the spectrums
E_max = 3; % Maximum energy of the spectrums
Total_bins=1000; % number of bins in input spectrum
bar = 1e-2; % cutoff;
%--------------------------------------------------------------------------
% PILE UP PROCESS
%--------------------------------------------------------------------------

% the input spectrum
E=linspace(E_min, E_max,Total_bins); % energy array of input spectrum
input_spectrum=exp(-(E-1).^2/0.05^2); % input spectrum

%normalized input spectrum
normalized_input_spectrum = normalize(input_spectrum,E); 

% pile up
%output spectrum
output_spectrum = pileup(normalized_input_spectrum,E,count_rate,tr,tf);
%normalized output spectrum
normalized_output_spectrum = normalize(output_spectrum,E);


%--------------------------------------------------------------------------
% PLOT
%--------------------------------------------------------------------------
figure
% input spectrum with pile up
semilogy(E,max(normalized_input_spectrum,bar), 'LineWidth',2);
hold on
% output spectrum with pile up
semilogy(E,max(normalized_output_spectrum,bar), 'LineWidth',2);
hold off

title('2 photon trapezoidal shape, Count Rate = '+string(count_rate)+ ...
    ', Rise time = '+string(tr)+', Flat-top time = '+string(tf));
ylabel('Probablity Distribution', 'FontSize',14);
xlabel('Energy',  'FontSize',14);
grid on;
grid minor;
lgd=legend('raw input spectrum','piled up output spectrum');
lgd.FontSize = 14;

%--------------------------------------------------------------------------
% METHODS
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% piles up a spectrum given probablity distribution, p, count rate, u and
% rise time tr, flat top tf
%--------------------------------------------------------------------------
function y = pileup(p,E,u,tr,tf)
    td = tr+tf; % total dead time
    a = tr/(tf+tr); %triangularity
    y = (1-u*td)*p + u*td*p_2photon(p,E,a);
end

%--------------------------------------------------------------------------
% pile up contribution from two photon in a spectrum for a probablity
% distribution, p, and triangularity, a
%--------------------------------------------------------------------------
function y = p_2photon(p,E,a)
        y = (1-a)*p_A(p,E)+a*p_B(p,E);
end 

%--------------------------------------------------------------------------
% first part of the integration, the rectangular contribution
% p_A = int^E_0 p(E)*p(E-E')dE'
% o(N^2) time
%--------------------------------------------------------------------------
function y = p_A(p,E)
	y=linspace(0,0,length(E)); % empty array
    dE = E(2)-E(1);
    % start the loop for convolution integration 
    for i = 2:length(E)
        for j = 1:i-1
            I = p(i-j)*p(j)*dE; % convolution
            y(i)=y(i)+ I; % update the array using dynamic programming
        end
    end
end

%--------------------------------------------------------------------------
% second part of the integration, the triangular contribution
% p_B = int^E_(E/2) int^E'_(E-E') p(E')*p(E'')/E'' dE''dE' 
% using dynamic programming programming 
% p_B(E+dE) = p_B(E) + 2*A(E)dE-2*B(E)dE  
% takes O(N) time
% A(E)= p(E) int^E_0 p(E')/E' dE'
% B(E)= int^E_(E/2) p(E')p(E-E')/(E-E') dE'
% both integration takes O(N) time
% in total the integration takes o(N^2)
%--------------------------------------------------------------------------
function y = p_B(p,E)
    y=linspace(0,0,length(E)); % empty array
    dE = E(2)-E(1);
    for i = 1:length(E)-1
		%add this region
		addition=0;
        for j = 1:i+1
			addition = addition + p(i+1)*p(j)/E(j)*dE;
        end
		%substract this region
		subtraction=0;
        for j = floor(i/2)+1:i
			subtraction = subtraction  + p(j)*p(i+1-j)/E(i+1-j)*dE;
        end
		y(i+1) = y(i) + 2*(addition - subtraction)*dE;
    end
end 

%--------------------------------------------------------------------------
% normalizes a function
%--------------------------------------------------------------------------
function y_n = normalize(y,E)
    dE = E(2)-E(1);
    y_n = y/(sum(y)*dE);
end