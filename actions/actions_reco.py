import ultralytics
from ultralytics import YOLO
import numpy as np
import cv2
import torch
from collections import Counter
# from torchvision.ops import box_iou 
# from collection import queue 
class Actions_recognition:
    def __init__(self,model_path):
        self.model=YOLO(model_path)

    def detect(self,frames):
        batch =20
        detections=[]
        for frame in range(0,len(frames),batch):
            detections+=self.model.predict(frames[frame:frame+20])
        return detections
    def show_action(self,temp,video_frames):
        
        pass  
    def apply_sorting(self,temp):
        temp_sorted = []

        for preds in temp:
            if preds == ['-'] or preds == []:
                temp_sorted.append('-')
            else:
                sorted_preds = sorted(preds, key=lambda x: x[1], reverse=True)
                temp_sorted.append(sorted_preds[0][0])
        return temp_sorted
    def class_founder(self,temp_window,threshold=3):
            counts = Counter(temp_window)
            for key, count in counts.items():
                if key=="set" or key =="defense" or key == "dig": # as these are very less predicted 
                    return key
                if key != '-' and count >= threshold:
                    return key
            return '-'  
    def final_actions(self,temp):
        window = 5
        threshold = 3
        events = []

        for i in range(len(temp) - window + 1):
            sub_window = temp[i:i+window]
            result = self.class_founder(sub_window, threshold)
            events.append(result)
        return events
    def get_action_tracks(self,video_frames,tracks):
        detections  = self.detect(video_frames)
        temp = []
        for frame_num,detection in enumerate(detections):
            class_names = detection.names
            print(f"frame no - {frame_num}")
            tem = []
            if detection.boxes is not None and len(detection.boxes)>0:
                bbox_boxes = detection.boxes.cpu()
                for i ,boxes in enumerate(bbox_boxes):
                    cls = int(detection.boxes.cls[i].item())
                    conf = float(detection.boxes.conf[i].item())
                    label = class_names[cls] if class_names else str(cls)
                    print(f"Detected: {label} with confidence {conf:.2f}")
                    tem.append([label,conf])
            else:
                tem.append("-")
            temp.append(tem)
        temp = self.apply_sorting(temp)
        temp = self.final_actions(temp)
        frames = []
        for frame_num , act in enumerate(temp):
            frame =video_frames[frame_num].copy()
            h,w = frame.shape[:2]
            if act !='-':
                text = temp[frame_num]
                cv2.rectangle(frame, (w//2, 100), (w//2 + 100, 200), (255, 0, 0), 2)
                cv2.putText(frame, text, (w//2 +50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),1)
            frames.append(frame)
        return frames



    # def get_action_tracks(self, video_frames, tracks):
    #     detections = self.detect(video_frames)

    #     for frame_num, detection in enumerate(detections):
    #         print(f"\n---- Frame {frame_num} ----")
    #         class_names = detection.names

    #         if detection.boxes is not None:
    #             det_boxes = detection.boxes.xyxy.cpu()
    #             for i, box in enumerate(det_boxes):
    #                 cls = int(detection.boxes.cls[i].item())
    #                 conf = float(detection.boxes.conf[i].item())
    #                 label = class_names[cls] if class_names else str(cls)
    #                 print(f"Detected: {label} with confidence {conf:.2f}")

    #                 # Compare with tracked players for this frame
    #                 player_boxes = []
    #                 player_ids = []
    #                 for track_id, player in tracks["players"][frame_num].items():
    #                     player_boxes.append(torch.tensor(player["bbox"]))
    #                     player_ids.append(track_id)

    #                 if player_boxes:
    #                     player_boxes = torch.stack(player_boxes)
    #                     ious = box_iou(box.unsqueeze(0), player_boxes).squeeze(0)

    #                     best_match_idx = torch.argmax(ious).item()
    #                     best_iou = ious[best_match_idx].item()

    #                     if best_iou > 0.5:
    #                         matched_id = player_ids[best_match_idx]
    #                         print(f"--> Matched with track ID {matched_id} (IoU: {best_iou:.2f})")

    # def get_action_tracks(self,video_frames,tracks):
        # detections = self.detect(video_frames)
        # for detect in detection:
        #     print("---------------st-------------------")
        #     print(detect)
        # for frame_num,detection in enumerate(detections):
        #     class_names = detection.names
        #     if detection.boxes is not None:
        #         for i in range(len(detection.boxes)):
        #             cls = int(detection.boxes.cls[i].item())
        #             conf = float(detection.boxes.conf[i].item())
        #             label = detection.names[cls] if hasattr(detection, "names") else str(cls)
        #             print(f"Detected: {label} with confidence {conf:.2f}")
        #             for track_id,player in tracks["players"][frame_num].items():
        #                 if detection.boxes[i].xyxy == player["bbox"]:
        #                     print("match found")

        #         for box in detection.boxes.xyxy:
        #             bbox = box.cpu().numpy().tolist()

        #             print(f"  ")
        #     else:
        #         tracks["players"][frame_num]

        #     print(f"at this frame {frame_num} -found -")
        #     for track_id , player in tracks["players"][frame_num].items():
        #         x1,y1,x2,y2 = player["bbox"]
                
        #         if (x1==)
        #         print(f"player id - {track_id} - bbox = {player['bbox']} ")


        # detect using bbox of each  player  (result - falied brutally :( )
        # for frame_num , frame in enumerate(video_frames):
        #     print("frame number - ",frame_num)
        #     for track_id,player in tracks["players"][frame_num].items():
        #         x1,y1,x2,y2 = player["bbox"]
        #         player_img = frame[int(y1):int(y2),int(x1):int(x2)]
        #         color_img = cv2.cvtColor(player_img,cv2.COLOR_BGR2RGB)
        #         result = self.model.predict(color_img)[0]
        #         print(f" player no {track_id} action taken - ")
        #         if result.boxes is not None:
        #             for i in range(len(result.boxes)):
        #                 cls  = int(result.boxes.cls[i].item())
        #                 conf = float(result.boxes.conf[i].item())
        #                 label = result.names[cls] if hasattr(result, "names") else str(cls)
        #                 print(f"Detected: {label} with confidence {conf:.2f}")
        #         else:
        #             print("no action")


            
            
                

    