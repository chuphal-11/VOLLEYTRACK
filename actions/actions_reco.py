import ultralytics
from ultralytics import YOLO

class Actions_recognition:
    def __init__(self,model_path):
        self.model=YOLO(model_path)

    def detect(self,frames):
        batch =20
        detections=[]
        for frame in range(0,len(frames),batch):
            detections+=self.model.predict(frames[frame:frame+20])
        return detections
    
    def get_action_tracks(self,video_frames):
        detections = self.detect(video_frames)
        # for detect in detection:
            # print("---------------st-------------------")
            # print(detect)
        for frame_num,detection in enumerate(detections):
            class_names = detection.names
            print("----------st------------")
            print(frame_num)
            if detection.boxes is not None:
                for box in detection.boxes:
                    print(box)
            else:
                print("none")
    