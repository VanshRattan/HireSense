def generate_feedback(audio_analysis_result: dict, video_analysis_result: dict = None):
    """
    Generates a mock feedback report based on the analysis.
    In a real app, this might use an LLM for deeper insights.
    """
    filler_count = audio_analysis_result.get("filler_word_count", 0)
    
    # Basic scoring logic
    communication_score = max(0.0, 100.0 - (filler_count * 2.5))
    confidence_score = 85.0 # Mock base score, can be updated with video
    
    if video_analysis_result:
        # Incorporate eye contact, etc.
        eye_contact = video_analysis_result.get("eye_contact_percentage", 100)
        confidence_score = (confidence_score + eye_contact) / 2
        
    summary = f"You used {filler_count} filler words. "
    if filler_count > 5:
        summary += "Try to pause silently instead of using 'um' or 'like'. "
    else:
        summary += "Great job keeping filler words to a minimum! "
        
    return {
        "communication_score": communication_score,
        "confidence_score": confidence_score,
        "filler_word_count": filler_count,
        "filler_words_used": audio_analysis_result.get("filler_words_used", {}),
        "feedback_summary": summary,
        "transcript": audio_analysis_result.get("transcript", "")
    }
