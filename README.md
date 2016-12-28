# resynthesizer

Creates a creepy and robotic sounding audio file from an existing wav file. Works by first slicing the file to small segments of specified size, applying fast fourier transform to each slice to transorm them into the frequency domain, approximating the original signal based on the frequencies and finally combining the slices. Work in progress.
