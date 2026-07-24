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
    
    # WPM Calculation
    duration = audio_analysis_result.get("duration", 1.0)
    # Average WPM = (words / duration_in_seconds) * 60
    wpm = (word_count / duration) * 60 if duration > 0 else 0
    wpm = round(wpm, 1)

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
        
    if wpm > 170:
        mistakes.append(f"You were speaking way too fast at {wpm} Words Per Minute.")
        improvements.append("Action: Slow down! A rushed pace projects anxiety. Aim for a conversational 130-150 WPM.")
    elif wpm > 0 and wpm < 100:
        mistakes.append(f"You were speaking very slowly at {wpm} Words Per Minute.")
        improvements.append("Action: Speed up your delivery slightly to sound more energized and engaged. Aim for 130-150 WPM.")
    elif wpm > 0:
        improvements.append(f"Action: Your speaking pace is excellent ({wpm} WPM). Perfect rhythm.")
    
    if not mistakes:
        summary = "Outstanding job! Your delivery was concise, confident, and professional with excellent pacing and eye contact.\n\n"
    else:
        summary = "### Mistakes Identified:\n- " + "\n- ".join(mistakes) + "\n\n"
        summary += "### What you should do to improve:\n- " + "\n- ".join(improvements) + "\n\n"

    # Perfect Answer Rewrite (Dual-LLM Integration: Groq + Gemini)
    import os
    import urllib.request
    import json
    
    groq_key = os.environ.get("GROQ_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if groq_key and len(transcript.strip()) > 5:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{
                    "role": "user",
                    "content": f"Rewrite the following interview answer to sound highly professional, extremely confident, and concise, eliminating all filler words but keeping the original core meaning. Do not include any explanations or intro text, just output the revised answer:\n\n{transcript}"
                }]
            }
            # Adding User-Agent to bypass Cloudflare 1010 blocking for raw urllib requests
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {groq_key}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            res = urllib.request.urlopen(req, timeout=12)
            res_json = json.loads(res.read())
            perfect_answer = res_json['choices'][0]['message']['content']
            summary += f"\n\n### Wait, how could I have said this better?\nHere is what you *should* have said instead:\n\n\"{perfect_answer.strip()}\""
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"Groq API HTTP Error [{e.code}]: {error_body}")
            summary += f"\n\n*(Could not generate the perfect rewrite due to a Groq API Error: {error_body}).* \n\n"
        except Exception as e:
            print(f"Groq Route Failed: {e}")
            summary += "\n\n*(Could not generate the perfect rewrite because the Groq API was unreachable).* \n\n"
            
    elif gemini_key and len(transcript.strip()) > 5:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": f"Rewrite the following interview answer to sound highly professional, extremely confident, and concise, eliminating all filler words but keeping the original core meaning. Do not include any explanations or intro text, just output the revised answer:\n\n{transcript}"}]}]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            res = urllib.request.urlopen(req, timeout=12)
            res_json = json.loads(res.read())
            perfect_answer = res_json['candidates'][0]['content']['parts'][0]['text']
            
            summary += f"\n\n### Wait, how could I have said this better?\nHere is what you *should* have said instead:\n\n\"{perfect_answer.strip()}\""
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"Gemini API HTTP Error [{e.code}]: {error_body}")
            if e.code == 429:
                summary += "\n\n*(Could not generate the perfect rewrite due to a Google API Quota/Rate Limit on your account. Please wait 1 minute and try again).* \n\n"
            else:
                summary += f"\n\n*(Gemini API Error {e.code}: Please check your backend terminal for details).* \n\n"
        except Exception as e:
            print(f"Gemini LLM Rewrite Failed: {e}")
            summary += "\n\n*(Could not generate the perfect rewrite because the Gemini API was unreachable).* \n\n"
            
    elif not gemini_key and not groq_key:
        summary += "\n\n*(Tip: Add a GROQ_API_KEY or GEMINI_API_KEY to your .env file to let the AI rewrite your answers perfectly!)* \n\n"
        
    return {
        "communication_score": round(communication_score, 1),
        "confidence_score": round(confidence_score, 1),
        "filler_word_count": filler_count,
        "filler_words_used": audio_analysis_result.get("filler_words_used", {}),
        "feedback_summary": summary,
        "transcript": transcript,
        "wpm": wpm
    }
