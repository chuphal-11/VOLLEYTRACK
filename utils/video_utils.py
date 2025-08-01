import cv2

def read_video(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        status, frame = cap.read()
        if not status:
            break
        frames.append(frame)
    cap.release()
    if len(frames) == 0:
        print(f"[ERROR] No frames read from: {path}")
    else:
        print(f"[INFO] Read {len(frames)} frames from: {path}")
    return frames

def save_video(output_video_frames, output_video_path):
    if not output_video_frames:
        print(f"[ERROR] No frames to save in {output_video_path}")
        return
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    h, w = output_video_frames[0].shape[:2]
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (w, h))
    for frame in output_video_frames:
        out.write(frame)
    out.release()
    print(f"[INFO] Saved video to {output_video_path}")
