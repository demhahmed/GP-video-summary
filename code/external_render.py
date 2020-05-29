import time
import subprocess
import glob

times = []

optimized = []

with open("render_before", mode="r") as file:
    lines = file.readlines()
    for line in lines:
        start, end = line.strip().split(" ")
        start = float(start)
        end = float(end)
        if len(optimized ) > 0:
            if abs( int(start) - optimized[-1][1] ) <= 10:
                optimized[-1][1] = int(end)
            else:
                optimized.append([int(start), int(end)])
        else:
            optimized.append([int(start), int(end)])


# with open("render_before", mode="r") as file:
#     lines = file.readlines()
#     for line in lines:
#         start, end = line.strip().split(" ")
#         times.append((float(start), float(end)))

times = optimized

filenames = []
cnt = 1
for start, end in times:
    # curr_time = time()
    subprocess.run(["ffmpeg", "-ss", str(start), "-i", "liverpool_vs_brighton_1.mp4",
                    "-c", "copy", "-t", str(end - start), f"/home/moamen/Desktop/GitHub/GP-video-summary/code/videos/{cnt}.mp4"])
    # filenames.append(f"{curr_time}.mp4")
    cnt += 1

time.sleep(10)

filenames = glob.glob("videos/*.mp4")

filenames.sort(key=lambda filename: int(filename.split(".")[0].split("/")[1]))

with open("my_list.txt", mode="w") as file:
    for path in filenames:
        file.write(f"file {path}\n")

subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i",
                "my_list.txt", "-c", "copy", "ffmpeg_out.mp4"])
