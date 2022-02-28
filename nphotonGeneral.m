%--------------------------------------------------------------------------
%                           DESCRIPTION: 
%--------------------------------------------------------------------------
% This program uses dynamic programming to simulate actual voltage for a
% given spectrum by creating a lot of trapezoidal pulses at random times
% with randomly generated energy heights from the energy spectrum. It then
% updates the voltage array by adding pulses over the range it spans. Then
% a method is used to detect peaks in the spectrum and the peaks are
% registered as photon counts with energy at peak height. Then the piled up
% spectrum is created from the detected peaks. This is the most general
% possible program designed to handle arbitary shaped pulse, count rate,
% and arbitary spectrum. 
%--------------------------------------------------------------------------
% Time complexity: Resolution means number of sites within a unit time
%------voltage creation-------peak detection----spectrum creation
% O(pulse number*resolution + Time*resolution + number of peaks)
% number of peak < Time*resolution
% so time complexity is O(pulse number*resolution+Time*resolution)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% PARAMETERS
%--------------------------------------------------------------------------
% specified parameters
E_0=1; % constant involving raw input
s=0.1; % constant involving raw input
pulse_rate = 100; % this is pulse per unit time
name = 'highcount_100_2.txt';
pulse_number = 10000000;

0; % this is total number of pulses
tr=1.0;%0.2/(0.2+0.012); % rise time
tf=0.0;%0.012/(0.2+0.012); % flat top time
resolution = 10; % number of bins in unit time
E_min = 0; % Minimum energy of the spectrums
E_max = 140; % Maximum energy of the spectrums
Total_bins=1000; % 
% number of bins in input spectrum
baseline=1e-9; % start counting only when baseline is crossed

%--------------------------------------------------------------------------
% PILEUP PROCESS
%--------------------------------------------------------------------------
Time = round(pulse_number/pulse_rate);  % time to run the experiment
t=linspace(0,Time, Time*resolution); % time array 
E=linspace(E_min, E_max,Total_bins); % energy array of input spectrum

% the input spectrum
% gaussian was chosen with average E_0 and stdev s. 
input_spectrum = exp(-(E-1).^2/0.1^2)+exp(-(E-0.5).^2/0.1^2);

% simulate the process and get output_spectrum, voltage array, and peaks
[output_spectrum, voltage, detected] = MonteCarlo(input_spectrum, E, ...
    t, tr, tf, pulse_rate,baseline);

%--------------------------------------------------------------------------
% NORMALIZE AND SMOOTHS THE SPECTRUMS TO COMPARE THEM
%--------------------------------------------------------------------------
% normalizes the input spectrum
normalized_input_spectrum = normalize(input_spectrum,E);
% normalize the output
normalized_output_spectrum = normalize(output_spectrum,E);
%smooths the normalized real spectrum
smooth_input_spectrum = smooth_cutoff(normalized_input_spectrum);
%smooths the normalized output spectrum
smooth_output_spectrum = smooth_cutoff(normalized_output_spectrum);

%--------------------------------------------------------------------------
% PLOTTING THE GRAPHS
%--------------------------------------------------------------------------
figure_title='Total time = '+string(Time)+', Count Rate = '+...
string(pulse_rate)+', Rise time = '+string(tr)+', Flat-top time = '+...
string(tf)';

% plot voltage(t) vs time
number_of_first_pulses = 100; % number of pulses we want to see
plot_voltage(t,voltage,detected,pulse_number,number_of_first_pulses);
figure_labels('Time','voltage(t)','voltage(t)','peaks',figure_title)

% plot Energy vs spectrums (normalized)
plot_spectrum(E,smooth_input_spectrum,smooth_output_spectrum);
figure_labels('Energy','Probablity Distribution','Raw Spectrum', ...
    'Piled Up Spectrum',figure_title)
%--------------------------------------------------------------------------
% CREATING THE FILE FROM THE DATA
%--------------------------------------------------------------------------
path='/Users/taosifahsan/Desktop/PPPL_Pulsepileup/New_works/Data/';
fileID = fopen([path  name],'w');
fprintf(fileID,'%f\n',smooth_output_spectrum);
fclose(fileID);

%--------------------------------------------------------------------------
% THESE ARE METHODS
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% CENTRAL METHODS
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% This simulates the monte carlo to produce the piled up spectrum, voltage
% and peaks. This is the core of the code and can be called to simulate the
% process as desired. The shape of the pulse can be controlled through tr,
% tf. The time to run the code can be controlled through t. pulse rate and
% sets the number of pulses we will simulate and their density. E and
% input_spectrum are the raw pile up less data that we will use late. 
%%-------------------------------------------------------------------------
function [output_spectrum, voltage, detected] = MonteCarlo( ...
    input_spectrum, E, t, tr, tf, pulse_rate,baseline)
    
    % total number of pulse
    Time = t(length(t));
    pulse_number = round(Time*pulse_rate);
    % create the voltage array 
    voltage = voltage_output(input_spectrum, E, t,tr,tf,pulse_number);
    % detect the peaks in the voltage array
    guess_length=round(pulse_number*pulse_rate);
    [peak, detected] = peak_detector(t,voltage,guess_length,baseline);
    % creates the output spectrum from the detected peaks
    output_spectrum = piled_up_spectrum(peak, E);  
end

%--------------------------------------------------------------------------
% this creates the voltage array, O(pulse_number*jd)
%--------------------------------------------------------------------------
function voltage = voltage_output(input_spectrum,E,t,tr,tf,pulse_number)
    Time = t(length(t)); % Total time for experiments
    resolution = round(length(t)/Time);
    voltage=t.*0.0; % empty voltage array
    td=2*tr+tf; %total time length of a pulse 
    jd=round(td*resolution);% total number of bins in a pulse
    dE= E(2)-E(1); % smoothness of the 

    P=input_spectrum/sum(input_spectrum); % probablity weight
    % this returns an height from the input function
    Energy_random_raw = randsample(E, pulse_number, true, P);

    for i = 1:pulse_number
	    % we smooth it out more
	    Energy_random = Energy_random_raw(i)+rand*dE-dE/2;
	    ti=rand*(Time-td); % choses a random time
        ji=round(ti*resolution); % site of that random time

	    % the elements that needs to be updated
	    t_temp=linspace(ti, ti+td, jd);
	    % creating the trapezoid 
	    y=trap(Energy_random, t_temp, ti, tr, tf);
	    % update the necessary elements by adding the trapezoid to it
        voltage(ji+1:ji+length(y))=voltage(ji+1:ji+length(y))+y;
    end
end 

%--------------------------------------------------------------------------
% this returns a trapezoid for given height, position,
% rise and flat top time
%--------------------------------------------------------------------------
function y = trap(h,t_temp,ti,tr,tf)
    % the rising part of the pulse
    A = ((t_temp-ti)/tr*h); 
	part1 =(ti<t_temp).*(t_temp<=ti+tr).* A; 
    % the flat top part of the pulse
	part2 =(ti+tr<t_temp).*(t_temp<=ti+tr+tf).*h;
    % the falling part of the pulse
    B = ((2*tr+tf+ti-t_temp)/tr*h);
	part3 =(tr+tf+ti<t_temp).*(t_temp<=2*tr+tf+ti).* B;
    % the full trapezoid
	y = part1+part2+part3;
end

%--------------------------------------------------------------------------
% this detects the peaks in voltage array,  O(Time*Resolution)
% "peak" gives us just of the peaks and is used in creating spectrum
% "detected" gives us where the peaks were found in order to plot them
%--------------------------------------------------------------------------
function [peak, detected] = peak_detector(t,voltage,guess_length,baseline)
    % create a temporary registry for peaks with a guessed length
    peak_temp=linspace(0,0,guess_length); 
    peak_detected= 0; % the initial pulse
    detected = t*0;
    i=1; % initial time
    while(i<length(t))
	    % if voltage starts to rise start looking for peak
        if voltage(i+1)>voltage(i)+baseline
		    j=0;
		    % look until it starts to fall
            while voltage(i+j+1)>voltage(i+j)-baseline && i+j+1<length(t)
			    j=j+1;
            end
		    % it fell so peak is found
		    i=i+j;
		    % if number of peaks are too high then resize the array
            if peak_detected >= guess_length
                % double the size
                guess_length=2*guess_length;
                peak_temp=resize(peak_temp,guess_length);
            end
            % update number of peaks detected
            peak_detected=peak_detected+1; 
            % register the peak
		    peak_temp(peak_detected)=voltage(i);
            detected(i)=voltage(i);
            
        end
	    i=i+1;
    end
    % splice the array to keep only the real counts
    peak = peak_temp(1:peak_detected); 
end
%--------------------------------------------------------------------------
% this resizes an array to length n, used in detect_peaks
%--------------------------------------------------------------------------
function y_n = resize (y,n)
    y_n = linspace(0,0,n);
    for i = 1:length(y)
        y_n(i)= y(i);
    end
end

%--------------------------------------------------------------------------
% this creates the piled up spectrum from the peaks detected O(len(peak))
%--------------------------------------------------------------------------
function spectrum = piled_up_spectrum(peak, E)
    %initial spectrum
    spectrum=linspace(0,0,length(E)); 
    % register counts and update the spectrum
    for i = 1:length(peak)
        % bin associated with peak
	    Energy_bin = round(peak(i)*(length(E)/(max(E)-min(E)))); 
        % increase count of that bean for every peak detected at that range
        if Energy_bin < length(E)
	        spectrum(Energy_bin+1)=spectrum(Energy_bin+1)+1; 
        end
    end
end


%--------------------------------------------------------------------------
% PLOT METHODS
%--------------------------------------------------------------------------
%--------------------------------------------------------------------------
% voltage vs time 
%--------------------------------------------------------------------------
function plot_voltage(t,voltage,detected,pulse_number,first_pulses)
    figure
    % portion of voltage we want to see or zoom
    first = round(first_pulses/pulse_number*length(t)); 
    % voltage 
    plot(t(1:first), voltage(1:first), 'LineWidth',2);
    hold on;
    % peaks
    plot(t(1:first),detected(1:first),'LineWidth',2);
   
end

%--------------------------------------------------------------------------
% Energy spectrum, both input (pile up less) and output (piled up)
%--------------------------------------------------------------------------
function plot_spectrum(E, smooth_input_spectrum,smooth_output_spectrum)
    figure
    % input spectrum with pile up
    semilogy(E,smooth_input_spectrum, 'LineWidth',2);
    hold on
    % output spectrum with pile up
    semilogy(E,smooth_output_spectrum, 'LineWidth',2);
    hold off
end

%--------------------------------------------------------------------------
% Label formalities
%--------------------------------------------------------------------------
function figure_labels(x_label,y_label,legend1,legend2,figure_title)
 hold off;
    title(figure_title);
    xlabel(x_label,  'FontSize',14);
    ylabel(y_label, 'FontSize',14);
    grid on;
    grid minor;
    lgd=legend(legend1,legend2);
    lgd.FontSize = 14;
end

%--------------------------------------------------------------------------
% EXTRA METHODS
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% helps in doing a moving average and smoothing the graph
%--------------------------------------------------------------------------
function y_smooth = mov_avg(y)
    w=[1,3,5,8,10,8,5,3,1]; % weigths of moving average
	y_smooth=y;

    for i = 1:length(y)-length(w)
		y_smooth(i+round(length(w)/2))=sum(y(i:i+length(w)-1).*w)/sum(w);
    end
end
%--------------------------------------------------------------------------
% cuts of graph below a lower limit and smooths it
%--------------------------------------------------------------------------
function y_n = smooth_cutoff(y)
    cutoff = 1e-3;
    bar = linspace(cutoff,cutoff,length(y));
	y_n = max(mov_avg(y),bar);
end
%--------------------------------------------------------------------------
% normalizes a function
%--------------------------------------------------------------------------
function y_n = normalize(y,E)
    dE = E(2)-E(1);
    y_n = y/(sum(y)*dE);
end