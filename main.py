import os
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt
os.chdir("/Users/User/Desktop") #change directory to file's location

def approx(r, d):
    """transforms a waveform to frequency domain using fft
        and approximates it with sine waves of different magnitude/frequency"""
    # apply fft
    transformed = fft(d)
    duration = len(transformed)/2
    
    # cut in half (symmetry) and get real part
    freq = transformed[:duration]
    freq = freq.real
    #freq = np.abs(freq)
    
    # combined magnitude of all frequencies
    total_mag = sum(np.abs(freq))

    # create new signal from fft
    synth = [0 for x in d] # empty np array   
    
    # populate with signals
    #for i in range(len(max_freq)):
    for i in range(len(freq)):
        # include every mth frequency in the approximation
        #   this seems to change the pitch of the final waveform
        m = 1
        if (i % m == 0):
            # create signal for current frequency
            samples = np.linspace(0, len(d), len(d))
            #print("Frequency: "+str(freq[i])+"Hz")
            signal = [freq[i]/total_mag*np.sin(2*np.pi*i*t) for t in samples]
            synth = np.add(synth, signal)
    return synth

# read wav file to np array
(rate, data) = wavfile.read("input.wav")
data = data.T[0] # comment this out of the input has only one track (mono)

# normalise
normalised = [x/(2**16.) for x in data]

# cut into slices
dt = 0.005
d_samples = int(dt*rate)

# list of slices
slices = []

# populate list with processed slices
n_slices = len(data) // d_samples
for i in range(0, len(data), d_samples):
    slices.append(normalised[i:i+d_samples])
    
# list for output waveform
output = []
for i in range(len(slices)):
    print(str(i+1)+"/"+str(len(slices)))
    output.extend(approx(rate, slices[i]))
    
# remove clicks
abs_output = [abs(x) for x in output]
average = sum(abs_output)/len(output)
output = [x for x in output if abs(x)<10*average]    
    
# normalize output track
output_max = max(output)
output = [x*(1./output_max) for x in output]

# write the final waveform as a wav file
wavfile.write("output.wav", rate, np.array(output))