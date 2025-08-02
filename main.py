from utils import read_video,save_video
from Tracker import Tracker
import supervision as sv
from actions import Actions_recognition

def main():
    video_frames = read_video('input_video/insta_video_1.mp4')
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames,read_from_sub_dir=True,path_of_sub_dir='Tracking_history/tracks.pkl')
    actions_r = Actions_recognition('models/action_detection.pt')
    video_frames = actions_r.get_action_tracks(video_frames,tracks)
    video_frames = tracker.draw_annotations(video_frames,tracks)
    save_video(video_frames,'output/add_action.avi')

if __name__ == '__main__':
    main()
