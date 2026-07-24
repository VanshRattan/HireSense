def generate_feedback(audio_analysis_result: dict, video_analysis_result: dict = None):
    """
    Generates a highly dynamic feedback report based on deeply integrated text and video heuristics.
    """
    filler_count = audio_analysis_result.get("filler_word_count", 0)
    transcript = audio_analysis_result.get("transcript", "")
    
    # Analyze the transcript content
    word_count = len(transcript.split()) if transcript else 0
    
    # Communication Score Calculation (Dynamic)
    # Start at 100, penalize for filler words relative to total words.
    filler_ratio = (filler_count / max(word_count, 1)) * 100
    communication_score = 100.0 - (filler_ratio * 4.0)  # Heavy penalty for dense filler usage
    
    if word_count < 10:
        communication_score -= 30  # Penalize for extremely short, one-word answers
    
    communication_score = max(0.0, min(100.0, communication_score))
    
    # Confidence Score Calculation (Dynamic)
    eye_contact = 100
    smile_frames = 50
    if video_analysis_result:
        eye_contact = video_analysis_result.get("eye_contact_percentage", 100)
        smile_frames = video_analysis_result.get("engagement_score", 50)
        
    # Confidence is determined heavily by eye contact and lack of filler words, entirely abandoning the generic "85" base.
    confidence_score = (eye_contact * 0.7) + (max(0, 100 - filler_ratio * 5) * 0.3)
    
    # Generate actionable improvements
    mistakes = []
    improvements = []
    
    if filler_ratio > 3:
        mistakes.append(f"You used {filler_count} filler words in a brief answer, making you sound uncertain.")
        improvements.append("Action: Try to practice taking a deep breath or a silent pause instead of using filler words to gather your thoughts.")
    else:
        improvements.append("Action: You controlled your filler words perfectly. Keep this up!")
        
    if eye_contact < 75:
        mistakes.append(f"Your eye contact was only {eye_contact}%. You were looking away too often.")
        improvements.append("Action: Remember to look directly at the camera lens, not just the screen, to simulate strong eye contact with the interviewer.")
        
    if word_count < 15:
        mistakes.append("Your response was extremely brief and lacked detail.")
        improvements.append("Action: Elaborate on your answers. Use the STAR method (Situation, Task, Action, Result) to build a captivating story.")
    
    if not mistakes:
        summary = "Outstanding job! Your delivery was concise, confident, and professional with excellent pacing and eye contact."
    else:
        summary = "### Mistakes Identified:\n- " + "\n- ".join(mistakes) + "\n\n"
        summary += "### What you should do to improve:\n- " + "\n- ".join(improvements)
        
    return {
        "communication_score": round(communication_score, 1),
        "confidence_score": round(confidence_score, 1),
        "filler_word_count": filler_count,
        "filler_words_used": audio_analysis_result.get("filler_words_used", {}),
        "feedback_summary": summary,
        "transcript": transcript
    }
