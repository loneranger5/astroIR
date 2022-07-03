import os
import sys

header = [3574, 1733, 386]
static_part = []
space = 386
pulse_0 = 490
pulse_1 = 1239

def encode(binary):
    signal=[]
    signal.extend(header)
    for i in binary:
        if int(i) == 0:
            signal.append(pulse_0)
        elif int(i) == 1:
            signal.append(pulse_1)
        signal.append(space)
    final_signal = ""
    byte_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    d = int('0b'+byte_chunks[14][::-1], 2)
    log_file = open("/home/renessmey/apps/astroboy/app.log", "a+")
    log_file.write(f"temp in encoder : {d}")
    if (d / 8 >=21):
        signal[131] = 9906
        signal[132] = 3582
        signal[133] = 1725
    else:
        signal[131]=9931
        signal[132]=3572
        signal[133]=1719
    for thing in signal:
        final_signal+=str(thing)+", "
    #final_signal = final_signal.pop(-1)
    print("Len of Signal ", len(signal))
    return  final_signal[:len(final_signal)-2]
