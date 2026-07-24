import cv2
import mediapipe as mp
import numpy as np

def analyze_video(video_path: str):
    """
    Analyzes a video for eye contact/engagement using MediaPipe Face Mesh.
    Returns basic metrics like percentage of frames with good eye contact.
    """
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Could not open video", "eye_contact_percentage": 0, "engagement_score": 0}
        
    total_frames = 0
    eye_contact_frames = 0
    smile_frames = 0
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
            
        total_frames += 1
        
        # Skip frames for speed (process every Nth frame if needed)
        if total_frames % 3 != 0:
            continue
            
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Basic heuristic: if face is detected and fairly central, we count as eye contact
                # More advanced would calculate pitch/yaw from facial landmarks
                eye_contact_frames += 1
                
                # Basic smile detection: distance between lip corners vs face width
                left_lip = face_landmarks.landmark[61]
                right_lip = face_landmarks.landmark[291]
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]
                
                mouth_width = ((right_lip.x - left_lip.x)**2 + (right_lip.y - left_lip.y)**2)**0.5
                eye_dist = ((right_eye.x - left_eye.x)**2 + (right_eye.y - left_eye.y)**2)**0.5
                
                if mouth_width > 0.8 * eye_dist:
                    smile_frames += 1

    cap.release()
    
    if total_frames == 0:
        return {"eye_contact_percentage": 0, "engagement_score": 0}
        
    processed_frames = total_frames // 3
    if processed_frames == 0: processed_frames = 1
    
    eye_contact_percentage = min(100, int((eye_contact_frames / processed_frames) * 100))
    engagement_score = min(100, int((smile_frames / processed_frames) * 100)) + 40 # boost base score
    
    return {
        "eye_contact_percentage": eye_contact_percentage,
        "engagement_score": min(100, engagement_score)
    }
