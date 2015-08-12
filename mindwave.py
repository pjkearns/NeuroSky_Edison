import serial
import struct
import time
import datetime
from datetime import datetime
from itertools import islice
import ctypes
import os
from decimal import *
# Data variables from mindflex
length      = 0
delta       = 0
theta       = 0
low_alpha   = 0
high_alpha  = 0
low_beta    = 0
high_beta   = 0
low_gamma   = 0
high_gamma  = 0
attention   = 0
meditation  = 0
poor_signal = 0
my_big_blob = ""
total_waves = 0
total_waves_total = 0
d_frac = 0
d_total = 0
t_frac = 0
t_total = 0
la_frac = 0
la_total = 0
ha_frac = 0
ha_total = 0
lb_frac = 0
lb_total = 0
hb_frac = 0
hb_total = 0
lg_frac = 0
lg_total = 0
hg_frac = 0
hg_total = 0
sample_count = 0
valsum = 0
record_on = False
record_val = 0

# Open com port to mindflex radio
print("Input desired sample size.")
samples_desired = int(raw_input("> "))
print("Okay, I will take %r samples.") % samples_desired
mindflex_serial = serial.Serial('/dev/rfcomm0', 57600) #timeout=.1
mindflex_serial.flushInput()
print("Opened mindflex COM port\n")

# Open log file
today = datetime.now()
#log_file = open(str(today.strftime("%y%b%d_%H%M%S")) + ".txt", "w")
#phone_file = open('/dev/rfcomm1/commands.txt', "w")
log_file = open("dump1.csv", "w")
log_file.write("delta,theta,low_a,high_a,low_b,high_b,low_g,high_g,att,med,chksum,total,,dfrac,tfrac,lafrac,hafrac,lbfrac,hbfrac,lgfrac,hgfrac\n")
# Sync state global variable
is_synced = False

def sync(): # Verified
    global is_synced # Need to modify a global variable in this function
    sync_bytes = 0
    while sync_bytes != 2:
        if unpack_a_byte() == 170:
            sync_bytes += 1
    is_synced = True

def parse():
    global is_synced # Need to modify a global variable in this function
    global sample_count
    global delta
    global theta
    global low_alpha
    global high_alpha
    global low_beta
    global high_beta
    global low_gamma
    global high_gamma
    global d_total
    global t_total
    global la_total
    global ha_total
    global lb_total
    global hb_total
    global lg_total
    global hg_total
    global total_waves_total
    global valsum
    global attention
    global meditation
    global la_frac
    global ha_frac

    if not is_synced:
        print("No Sync")
        return
    #packet = Packet()
    if is_synced:
        plength = unpack_a_byte()
        if plength == 170:
            is_synced = False
        elif plength == 32:
            i = 0
            while i <= plength:
                minddump = unpack_a_byte()
                if minddump == 131:
                    #log_file.write(str(minddump))
                    #log_file.write(",")
                    #log_file.write(str(i))
                    #log_file.write(",")
                    i += 1
                elif minddump == 24:
                    print("Got a new packet.\n")
		    #print(record_on)
                    #log_file.write(str(i))
                    #log_file.write(",")
                    delta = unpack_three_bytes()
                    d_total += delta
                    log_file.write(str(delta))
                    log_file.write(",")
                    theta = unpack_three_bytes()
                    t_total += theta
                    log_file.write(str(theta))
                    log_file.write(",")
                    low_alpha = unpack_three_bytes()
                    la_total += low_alpha
                    log_file.write(str(low_alpha))
                    log_file.write(",")
                    high_alpha = unpack_three_bytes()
                    ha_total += high_alpha
                    log_file.write(str(high_alpha))
                    log_file.write(",")
                    low_beta = unpack_three_bytes()
                    lb_total += low_beta
                    log_file.write(str(low_beta))
                    log_file.write(",")
                    high_beta = unpack_three_bytes()
                    hb_total += high_beta
                    log_file.write(str(high_beta))
                    log_file.write(",")
                    low_gamma = unpack_three_bytes()
                    lg_total += low_gamma
                    log_file.write(str(low_gamma))
                    log_file.write(",")
                    high_gamma = unpack_three_bytes()
                    hg_total += high_gamma
                    log_file.write(str(high_gamma))
                    log_file.write(",")
                    att_code = unpack_a_byte()
                    attention = unpack_a_byte()
                    log_file.write(str(attention))
                    log_file.write(",")
                    med_code = unpack_a_byte()
                    meditation = unpack_a_byte()
                    log_file.write(str(meditation))
                    log_file.write(",")
		    #phone_file.write(str(meditation))
		    #phone_file.write(",")
                    check_sum = unpack_a_byte()
                    log_file.write(str(check_sum))
                    log_file.write(",")
                    total_waves = delta + theta + low_alpha + high_alpha + low_beta + high_beta + low_gamma + high_gamma
                    total_waves_total += total_waves
                    log_file.write(str(total_waves))
                    log_file.write(",")
                    log_file.write("")
                    log_file.write(",")
                    getcontext().prec = 5
                    d_frac = Decimal(delta) / Decimal(total_waves)
                    log_file.write(str(d_frac))
                    log_file.write(",")
                    t_frac = Decimal(theta) / Decimal(total_waves)
                    log_file.write(str(t_frac))
                    log_file.write(",")
                    la_frac = Decimal(low_alpha) / Decimal(total_waves)
                    log_file.write(str(la_frac))
                    log_file.write(",")
                    ha_frac = Decimal(high_alpha)/Decimal(total_waves)
                    log_file.write(str(ha_frac))
                    log_file.write(",")
                    lb_frac = Decimal(low_beta)/ Decimal(total_waves)
                    log_file.write(str(lb_frac))
                    log_file.write(",")
                    hb_frac = Decimal(high_beta)/Decimal(total_waves)
                    log_file.write(str(hb_frac))
                    log_file.write(",")
                    lg_frac = Decimal(low_gamma)/Decimal(total_waves)
                    log_file.write(str(lg_frac))
                    log_file.write(",")
                    hg_frac = Decimal(high_gamma)/Decimal(total_waves)
                    log_file.write(str(hg_frac))
                    i += 29
                else:
                    i += 1
            log_file.write("\n")
            is_synced = False
            sample_count += 1
        else:
            i = 0
            while i <= plength:
                minddump = unpack_a_byte()
                i += 1
            is_synced = False
    return

def record():
    global la_frac
    global ha_frac
    alpha_total = la_frac + ha_frac
    global record_on
    global record_val
    if alpha_total >= 0.4:
        #print(record_on)
	record_val += 1
        if record_val == 2:
            record_on = not record_on
            if record_on == True:
		#phone_file.write("Recording")
                print("Recording.")
	
            else:
		#phone_file.write("Stopped")
                print("Stopped")
    else:

	record_val = 0
    return

def unpack_a_byte():
    byte = mindflex_serial.read(1)
    return struct.unpack('>B', byte)[0]

def unpack_three_bytes():
    my_three_bytes = mindflex_serial.read(3)

    three_bytes = ''.join([b for b in islice(my_three_bytes,0,3)])
    four_bytes = b'\x00' + three_bytes
    return struct.unpack('>I', four_bytes)[0]
    #return struct.unpack('>hb', my_three_bytes)[0]


print("Waiting for Data")

while True:
    if sample_count >= samples_desired:
        d_avg = Decimal(d_total) / Decimal(total_waves_total)
        t_avg = Decimal(t_total) / Decimal(total_waves_total)
        la_avg = Decimal(la_total) / Decimal(total_waves_total)
        ha_avg = Decimal(ha_total) / Decimal(total_waves_total)
        lb_avg = Decimal(lb_total) / Decimal(total_waves_total)
        hb_avg = Decimal(hb_total) / Decimal(total_waves_total)
        lg_avg = Decimal(lg_total) / Decimal(total_waves_total)
        hg_avg = Decimal(hg_total) / Decimal(total_waves_total)
        log_file.write("\n,,,,,,,,,,,,,delta,theta,lowA,highA,lowB,highB,lowG,highG")
        log_file.write("\n,,,,,,,,,,,,,")
        log_file.write(str(d_avg))
        log_file.write(",")
        log_file.write(str(t_avg))
        log_file.write(",")
        log_file.write(str(la_avg))
        log_file.write(",")
        log_file.write(str(ha_avg))
        log_file.write(",")
        log_file.write(str(lb_avg))
        log_file.write(",")
        log_file.write(str(hb_avg))
        log_file.write(",")
        log_file.write(str(lg_avg))
        log_file.write(",")
        log_file.write(str(hg_avg))
        if la_avg > d_avg:
            log_file.write("\n\n,,,,,,,,,,,,,you are doing a good job meditating")
        else :
            log_file.write("\n\n,,,,,,,,,,,,,meditation levels not high enough")
        mindflex_serial.close()
        print("Closed mindflex COM port")
        log_file.close()
        os.system("dump1.csv")
        break

    try:
        if not is_synced:
            sync()
        if is_synced:
            parse()
	    record()
        is_synced = False
        #print("delta: ", delta, " theta: ", theta, " low_alpha: ", low_alpha, " high_alpha: ", high_alpha, " low_beta: ", low_beta, " high_beta: ", high_beta, " low_gamma: ", low_gamma, " high_gamma: ", high_gamma, " poor signal: ", poor_signal, " attention: ", attention, " meditation: ", meditation)
        #log_file.write(str(mindflex_readings))
        #log_file.write("\n")

    except KeyboardInterrupt:
        mindflex_serial.close()
        print("Closed mindflex COM port")
        log_file.close()
        break

