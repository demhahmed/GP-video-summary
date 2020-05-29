import time

times = []

total_length = 0
cnt  = 0
with open("render_before", mode="r") as file:
    lines = file.readlines()
    for line in lines:
        start, end = line.strip().split(" ")
        end = float(end)
        start = float(start)
        times.append((time.strftime("%H:%M:%S", time.gmtime(start)), time.strftime("%H:%M:%S", time.gmtime(end))))

with open("time_seonds", mode="w") as file:
    for tup in times:
        file.write(tup[0] + '\t' + tup[1] + '\n')