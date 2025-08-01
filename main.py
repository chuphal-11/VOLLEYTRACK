from utils import read_video,save_video
from Tracker import Tracker
import supervision as sv
from actions import Actions_recognition
def main():
    video_frames = read_video('input_video/5_video_main.mp4')
    # tracker = Tracker('models/best.pt')
    actions_r = Actions_recognition('models/action_detection_2.pt')
    actions_r.get_action_tracks(video_frames)
    # tracks = tracker.get_object_tracks(video_frames,read_from_sub_dir=True,path_of_sub_dir='Tracking_history/tracks.pkl')
    # video_frames = tracker.draw_annotations(video_frames,tracks)
    # save_video(video_frames,'output/1_video.avi')
    pass

if __name__ == '__main__':
    main()
