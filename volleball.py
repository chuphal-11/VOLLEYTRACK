from ultralytics import YOLO

model = YOLO('models/player_no_detect.pt')

result = model.predict("input_video/7_video_main.mp4",save=True)
print(result[0])

for box in result[0].boxes:
    print(box)