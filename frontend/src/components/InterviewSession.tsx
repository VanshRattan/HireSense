"use client";

import { useState } from "react";
import { Mic, Video, StopCircle, RefreshCw, Send, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import axios from "axios";

export default function InterviewSession() {
  const [isRecording, setIsRecording] = useState(false);
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);

  const startRecording = () => {
    setIsRecording(true);
    // In a real app we would use navigator.mediaDevices.getUserMedia here
  };

  const stopRecording = async () => {
    setIsRecording(false);
    setLoading(true);
    
    try {
      // Mock API call to create session and trigger analysis
      const res = await axios.post("http://localhost:8000/sessions/start", { user_id: 1 });
      const sessionId = res.data.id;
      
      // We would normally upload the audio chunk here, then call finish
      // For now we mock the finish sequence (which expects an existing file in our backend, maybe this fails because we didn't upload a file)
      // Since it's a mock frontend, let's just show a fake result after delay
      setTimeout(() => {
        setSessionData({
          communication_score: 85,
          confidence_score: 90,
          filler_word_count: 3,
          feedback_summary: "Great job keeping filler words to a minimum! Try to maintain more consistent eye contact.",
          transcript: "Hello, thank you for having me. I am very excited about this opportunity."
        });
        setLoading(false);
      }, 3000);
      
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

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
            <div className={`w-full aspect-video rounded-2xl border-2 flex items-center justify-center transition-all duration-500 shadow-lg relative overflow-hidden ${isRecording ? 'border-red-500/50 bg-red-950/20' : 'border-indigo-500/30 bg-black/40'}`}>
              
              {isRecording ? (
                <div className="flex flex-col items-center">
                  <div className="relative">
                    <div className="absolute -inset-4 rounded-full bg-red-500/20 animate-ping"></div>
                    <Video className="w-16 h-16 text-red-500 animate-pulse" />
                  </div>
                  <p className="mt-4 text-red-400 font-medium">Recording in Progress...</p>
                  
                  {/* Mock Audio Visualizer */}
                  <div className="flex items-center justify-center gap-1 mt-6 h-12">
                    {[...Array(12)].map((_, i) => (
                      <motion.div
                        key={i}
                        className="w-1.5 bg-red-400 rounded-full"
                        animate={{ height: ["10%", "100%", "10%"] }}
                        transition={{
                          duration: Math.random() * 0.5 + 0.5,
                          repeat: Infinity,
                          ease: "easeInOut"
                        }}
                      />
                    ))}
                  </div>
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
                <p className="text-gray-400 leading-relaxed bg-white/5 p-4 rounded-lg">{sessionData.feedback_summary}</p>
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
