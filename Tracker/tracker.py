from ultralytics import YOLO
import os
import supervision as sv
import pickle
import cv2
import numpy as np
import sys
sys.path.append('../')
from utils import get_centre_of_bbox,get_bbox_width

class Tracker():
    def __init__(self,model):
        self.model = YOLO(model)
        self.tracker = sv.ByteTrack()
        

    def detect(self,video_frames):
        batch = 20
        detections = []
        for i in range(0,len(video_frames),batch):
            detections += self.model.predict(video_frames[i:i+20])
        return detections
    
    def get_object_tracks(self,video_frames,read_from_sub_dir=None,path_of_sub_dir=None,):
        if read_from_sub_dir and path_of_sub_dir is not None and os.path.exists(path_of_sub_dir):
            with open(path_of_sub_dir,'rb') as f:
                tracks = pickle.load(f)
            return tracks
        detections = self.detect(video_frames)

        tracks = {
                    'player': [],
                    'referee': [],
                    'ball':    []
                }


        for frame_num, detection in enumerate(detections):


            class_name = detection.names
            class_name_inv = dict()
            for key,value in class_name.items():
                class_name_inv[value]=key            

            detection_supervision = sv.Detections.from_ultralytics(detection)
            track_detection_supervision = self.tracker.update_with_detections(detection_supervision)
            
            tracks['player'].append({})
            tracks['referee'].append({})
            tracks['ball'].append({})
            # print("frame_nums-   ", frame_num )
            for tracks_detection_info in track_detection_supervision:
                class_id = tracks_detection_info[3]
                bbox = tracks_detection_info[0].tolist()
                tracker_id = tracks_detection_info[4]
                # print(" class_id  - ", class_id , "  bbox  -  ",bbox)
                if class_id == class_name_inv['player']:
                    tracks['player'][frame_num][tracker_id] = {'bbox':bbox}
                if class_id == class_name_inv['referee']:
                    tracks['referee'][frame_num][tracker_id] = {'bbox':bbox}
                if class_id == class_name_inv['ball']:
                    tracks['ball'][frame_num][1] = {'bbox':bbox}
            for track_detections_info in track_detection_supervision:
                bbox = track_detections_info[0].tolist()
                tracker_id  = tracks_detection_info[4]
                class_id = tracks_detection_info[3]
                if class_id == class_name_inv['ball']:
                    tracks['ball'][frame_num][1] = {'bbox':bbox} 
            # print("----------------------------------END-------------------------")
        if path_of_sub_dir is not None:
            with open(path_of_sub_dir,'wb') as f:
                pickle.dump(tracks,f)

        return tracks
        

    def draw_circle():
        pass
    def draw_elipse(self,frame,bbox,color,track_id):
        y2 = int(bbox[3])
        X_centre = get_centre_of_bbox(bbox)
        width = get_bbox_width(bbox)
        scaled_width = max(8, min(int(0.3 * width), 15))  # Clamp between 8 and 15
        cv2.ellipse(
            frame,
            center=(X_centre[0], y2-10),
            axes=(50,10),
            angle=0.0,
            startAngle=-35,
            endAngle=235,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4
        )
        
        # add track id in rectange in centre of elipse 
        rec_width = 40
        rec_height=20
        X1_rec= X_centre[0] - rec_width//2    
        X2_rec= X_centre[0] + rec_width//2
        Y1_rec= (y2-rec_height//2)  +15
        Y2_rec=  (y2+rec_height//2) +15
        if track_id is not None:
            cv2.rectangle(frame,
                          (int(X1_rec),int(Y1_rec)),
                          (int(X2_rec),int(Y2_rec)),color,cv2.FILLED)

            X1_text = X1_rec+12
            if track_id>99:
                X1_text-=10
            cv2.putText(frame,str(track_id),
                        (int(X1_text),int(Y1_rec+15)),
                        cv2.FONT_HERSHEY_COMPLEX,0.6
                        ,(0,0,0),2)
        return frame
    def draw_triange(self,frame,bbox,color):
        y = int(bbox[3])
        x,_ = get_centre_of_bbox(bbox)
        triangle_points = np.array([[x,y],[x-10,y-20],[x+10,y-20]])
        
        # inner color
        cv2.drawContours(frame,[triangle_points],0,color,cv2.FILLED)
        # border
        cv2.drawContours(frame,[triangle_points],0,(0,0,0),2)
        
        return frame
    
    def draw_annotations(self,frames,tracks):
        video_frames=[]

        for frame_num,frame in enumerate(frames):
            frame = frame.copy()
            # print("length of track player - - ",len(tracks['player'][frame_num]))
            player_dict = tracks['player'][frame_num]
            ball_dict = tracks['ball'][frame_num]
            for track_id,player in player_dict.items():
                bbox = player['bbox']
                color = (255,0,0)
                frame = self.draw_elipse(frame,bbox,color,track_id)
            for track_id,player in ball_dict.items():
                bbox = player['bbox']
                color = (255,0,0)
                color = (0,255,0)
                frame = self.draw_triange(frame,bbox,color )
            video_frames.append(frame)


        return video_frames