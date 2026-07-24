"use client";

import InterviewSession from "@/components/InterviewSession";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white overflow-hidden py-10 px-4">
      {/* Background decorations */}
      <div className="fixed inset-0 z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-900/20 blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/20 blur-[120px]"></div>
      </div>

      <div className="relative z-10 max-w-6xl mx-auto flex flex-col items-center">
        <header className="mb-12 text-center">
          <div className="inline-block p-1 px-3 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium mb-4">
            AI-Powered Interview Assessment
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4">
            Welcome to <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">HireSense</span>
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            Master your narrative. Get real-time AI feedback on your communication, eye contact, and confidence to ace your next technical or behavioral interview.
          </p>
        </header>

        <section className="w-full grid grid-cols-1 gap-8">
          <InterviewSession />
        </section>
      </div>
    </main>
  );
}
