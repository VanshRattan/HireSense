"use client";

import { useState, useRef, useEffect } from "react";
import { Mic, Video, StopCircle, RefreshCw, Send, CheckCircle, Camera } from "lucide-react";
import { motion } from "framer-motion";
import axios from "axios";

export default function InterviewSession() {
  const [isRecording, setIsRecording] = useState(false);
  const [sessionData, setSessionData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      chunksRef.current = [];
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();

      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing media devices.", err);
      alert("Please allow camera and microphone access to start the interview.");
    }
  };

  const stopRecording = async () => {
    if (!mediaRecorderRef.current) return;

    setIsRecording(false);
    setLoading(true);

    // Stop recorder and wait for final blob
    const stopPromise = new Promise<Blob>((resolve) => {
      mediaRecorderRef.current!.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        resolve(blob);
      };
      mediaRecorderRef.current!.stop();
    });

    // Stop all media tracks visually
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    try {
      const recordedBlob = await stopPromise;
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

      // 1. Start Session
      const startRes = await axios.post(`${API_URL}/sessions/start`, { user_id: 1 });
      const sessionId = startRes.data.id;

      // 2. Upload Video
      const formData = new FormData();
      formData.append("file", recordedBlob, "interview_video.webm");
      await axios.post(`${API_URL}/sessions/${sessionId}/upload`, formData);

      // 3. Process and Finish
      const finishRes = await axios.post(`${API_URL}/sessions/${sessionId}/finish`);

      // Load real AI report!
      setSessionData(finishRes.data);
      setLoading(false);

    } catch (error) {
      console.error(error);
      alert("Failed to analyze video. Check console for details.");
      setLoading(false);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[600px] w-full max-w-4xl mx-auto backdrop-blur-xl bg-white/10 dark:bg-black/30 border border-white/20 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
      {/* Decorative gradient orb */}
      <div className="absolute -top-32 -left-32 w-64 h-64 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
      <div className="absolute -bottom-32 -right-32 w-64 h-64 bg-fuchsia-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>

      <div className="z-10 w-full flex flex-col items-center">
        <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400 mb-6">
          Mock Interview Session
        </h2>

        {!sessionData && !loading && (
          <div className="flex flex-col items-center w-full max-w-2xl">
            <div className={`w-full aspect-video rounded-2xl border-2 flex items-center justify-center transition-all duration-500 shadow-lg relative overflow-hidden ${isRecording ? 'border-red-500/50 bg-black/80' : 'border-indigo-500/30 bg-black/40'}`}>

              {/* The actual video feed container */}
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-500 ${isRecording ? 'opacity-100' : 'opacity-0'}`}
              />

              {isRecording ? (
                <div className="absolute top-4 right-4 flex items-center gap-2 px-4 py-1.5 bg-black/60 backdrop-blur-md rounded-full border border-red-500/50 shadow-xl z-10">
                  <div className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping"></div>
                  <span className="text-red-400 font-bold tracking-widest text-xs uppercase shadow-black drop-shadow-md">Live</span>
                </div>
              ) : (
                <div className="flex flex-col items-center text-gray-400">
                  <Video className="w-16 h-16 mb-4 opacity-50" />
                  <p>Ready to start your interview?</p>
                </div>
              )}
            </div>

            <div className="mt-8 flex gap-4">
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  className="px-8 py-3 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-semibold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-105 transition-all flex items-center gap-2"
                >
                  <Video className="w-5 h-5" /> Start Interview
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="px-8 py-3 rounded-full bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold shadow-lg shadow-red-500/30 hover:shadow-red-500/50 hover:scale-105 transition-all flex items-center gap-2"
                >
                  <StopCircle className="w-5 h-5" /> Finish & Analyze
                </button>
              )}
            </div>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <RefreshCw className="w-12 h-12 text-indigo-400 animate-spin mb-4" />
            <p className="text-indigo-200 text-lg font-medium">Analyzing your performance...</p>
            <p className="text-gray-400 text-sm mt-2">Transcribing and checking for filler words</p>
          </div>
        )}

        {sessionData && !loading && (
          <div className="w-full bg-black/40 border border-white/10 rounded-2xl p-8 backdrop-blur-md">
            <div className="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
              <CheckCircle className="text-emerald-400 w-8 h-8" />
              <h3 className="text-2xl font-bold text-white">Analysis Complete</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-gradient-to-br from-indigo-900/50 to-blue-900/50 p-6 rounded-xl border border-indigo-500/30">
                <p className="text-indigo-200 text-sm mb-1">Communication Score</p>
                <p className="text-4xl font-bold text-white">{sessionData.communication_score}%</p>
              </div>
              <div className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 p-6 rounded-xl border border-purple-500/30">
                <p className="text-purple-200 text-sm mb-1">Confidence Score</p>
                <p className="text-4xl font-bold text-white">{sessionData.confidence_score}%</p>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <h4 className="text-lg font-semibold text-gray-200 mb-2">Feedback Summary</h4>
                <p className="text-gray-400 leading-relaxed bg-white/5 p-4 rounded-lg whitespace-pre-wrap">{sessionData.feedback_summary}</p>
              </div>

              <div>
                <h4 className="text-lg font-semibold text-gray-200 mb-2">Transcript</h4>
                <p className="text-gray-400 leading-relaxed italic bg-white/5 p-4 rounded-lg border-l-4 border-indigo-500">"{sessionData.transcript}"</p>
              </div>
            </div>

            <div className="mt-8 flex justify-center">
              <button
                onClick={() => setSessionData(null)}
                className="px-6 py-2 rounded-full border border-white/20 text-white hover:bg-white/10 transition-colors"
              >
                Start New Session
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
