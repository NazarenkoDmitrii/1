import RPi.GPIO as G
import matplotlib.pyplot as plt
import time
G.setmode(G.BCM)

troyka = 13
leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
MaxVoltage = 3.3
bites = len(dac)
levels = 2 ** bites
V_did = []
data_v = []
time_for_graf = []

G.setup(dac, G.OUT, initial = G.LOW)
G.setup(troyka, G.OUT)
G.setup(leds, G.OUT, initial = G.LOW)
G.setup(comp, G.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    value_res = 0
    temp_value = 0
    for i in range(bites):
        pow2 = 2 ** (bites - i - 1)
        temp_value = value_res + pow2
        signal = decimal2binary(temp_value)
        G.output(dac, signal)
        time.sleep(0.008)
        compVal = G.input(comp)
        if compVal == 0:
            value_res = value_res + pow2
    G.output(leds, signal)
    return value_res


def charge_time(lim, dir):
    while True:
        value = adc()
        voltage = value / levels * MaxVoltage
        V_did.append(value)
        data_v.append(voltage)
        print("V = ", voltage)
        time_for_graf.append(time.time() - start_time)
        if voltage >= lim and dir == 1:
            break
        if voltage < lim and dir == -1:
            break

try:
    start_time = time.time()
    G.output(troyka, 1)
    charge_time(2.719, 1)
    G.output(troyka, 0)
    charge_time(2.27, -1)
    finish_time = time.time()

    print("\n  S: ", finish_time - start_time)
    print("\n Hz: ", len(V_did) / (finish_time - start_time))
    print("\n V: ", MaxVoltage / 256)
    
    V_str = [str(item) for item in V_did]
    with open("/home/b03-302/Desktop/data.txt", "w") as f:
        f.write("\n".join(V_str))

    L_str = [str(item) for item in time_for_graf]
    with open("/home/b03-302/Desktop/time.txt", "w") as f:
        f.write("\n".join(L_str))
    
    plt.plot(time_for_graf, data_v, 'k:')
    plt.xlabel("time, s")
    plt.ylabel("voltage, V")
    plt.show()

    disc = str(len(V_did) / (finish_time - start_time))
    kvant = str(MaxVoltage / 256)
    with open("/home/b03-302/Desktop/settings.txt","w") as set:
        set.write("Hz: " + disc)
        set.write("\n")
        set.write('V: ' + kvant)
finally:
    G.output(dac, 0)
    G.output(leds, 0)
    G.output(troyka, 0)
    G.cleanup()
