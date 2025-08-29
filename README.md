# 🏐 VolleyTrack

VolleyTrack is a **computer vision project** that tracks the volleyball and players in match recordings or clips.  
It also supports simple action recognition (like serve, pass, spike, etc.) and saves the processed outputs as videos.

## 📹 Demo Video
➡️![Demo](assets/video_1.gif)


## 📂 Project Structure
VOLLEYTRACK/
├── actions/
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-310.pyc
│   │   └── actions_reco.cpython-310.pyc
│   └── actions_reco.py
├── LICENSE
├── main.py
├── mod/
│   └── action_detection_3.pt
├── output/
│   ├── 1_simple st.avi
│   ├── 1_video.avi
│   ├── 2_add ball.avi
│   └── add_action.avi
├── README.md
├── Tracker/
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-310.pyc
│   │   └── tracker.cpython-310.pyc
│   └── tracker.py
├── Tracking_history/
│   ├── tracks_7.pkl
│   └── tracks.pkl
├── utils/
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-310.pyc
│   │   ├── bbox_utils.cpython-310.pyc
│   │   └── video_utils.cpython-310.pyc
│   ├── bbox_utils.py
│   └── video_utils.py
└── volleball.py

```
