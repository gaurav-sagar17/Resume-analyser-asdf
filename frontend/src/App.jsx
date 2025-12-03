import { useState } from 'react'
import { motion } from 'framer-motion'
import { Cpu, FileText, Sparkles } from 'lucide-react'
import FileUpload from './components/FileUpload'
import Loader from './components/Loader'
import ScoreDashboard from './components/ScoreDashboard'
import FeedbackCards from './components/FeedbackCards'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileUpload = async (file) => {
    setLoading(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setAnalysisResult(response.data)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'An error occurred while analyzing the resume',
      )
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setAnalysisResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8 bg-radial-spot">
      <div className="w-full max-w-6xl">
        {/* Top bar / hero */}
        <header className="flex items-center justify-between mb-8">
          <motion.div
            className="flex items-center gap-3"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className="relative h-10 w-10 rounded-2xl bg-slate-900/80 border border-slate-700 flex items-center justify-center overflow-hidden">
              <motion.div
                className="absolute inset-[1px] rounded-2xl bg-slate-900"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              />
              <motion.div
                className="absolute h-10 w-10 bg-ring-gradient opacity-60"
                style={{ filter: 'blur(10px)' }}
                animate={{ rotate: 360 }}
                transition={{ duration: 18, repeat: Infinity, ease: 'linear' }}
              />
              <Cpu className="relative z-10 w-4 h-4 text-cyan-300" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-semibold tracking-tight text-slate-50">
                Resume Analyzer
              </h1>
              <p className="text-xs md:text-sm text-slate-400 max-w-md">
                Upload your PDF and get a rule-based breakdown of skills, experience,
                education, and formatting. No AI — just clear, structured feedback.
              </p>
            </div>
          </motion.div>

          <motion.div
            className="flex flex-col items-end gap-1 text-xs"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.05 }}
          >
            <div className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-900/70 border border-slate-700/80 text-[11px] text-slate-300">
              <Sparkles className="w-3 h-3 text-amber-300" />
              <span className="uppercase tracking-[0.16em]">
                Rule-based scoring
              </span>
            </div>
            <span className="text-[11px] text-slate-500">
              FastAPI · React · TailwindCSS
            </span>
          </motion.div>
        </header>

        {/* Main glass card */}
        <motion.div
          className="relative bg-slate-950/70 border border-slate-800/80 rounded-3xl shadow-glass-xl backdrop-blur-2xl p-6 md:p-8 space-y-6 overflow-hidden"
          initial={{ opacity: 0, y: 24, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.45, ease: 'easeOut' }}
        >
          <div className="pointer-events-none absolute inset-0 opacity-40">
            <div className="absolute -top-24 -left-10 h-40 w-40 bg-ring-gradient rounded-full blur-3xl" />
            <div className="absolute -bottom-32 right-0 h-52 w-52 bg-cyan-500/40 rounded-full blur-3xl" />
          </div>

          <div className="relative z-10 space-y-6">
            {!analysisResult && !loading && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35, delay: 0.05 }}
              >
                <FileUpload onFileUpload={handleFileUpload} error={error} />
                <div className="mt-3 flex items-center gap-2 text-[11px] text-slate-500">
                  <FileText className="w-3 h-3" />
                  <span>
                    Tip: use clear section headings (Skills, Experience, Education,
                    Projects) for the best analysis.
                  </span>
                </div>
              </motion.div>
            )}

            {loading && <Loader />}

            {error && !loading && (
              <motion.div
                className="bg-red-500/10 border border-red-500/40 text-red-200 px-4 py-3 rounded-xl mb-2 text-sm relative z-10"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Something went wrong</p>
                    <p className="text-xs mt-1 opacity-90">{error}</p>
                  </div>
                  <button
                    onClick={handleReset}
                    className="ml-4 px-3 py-1.5 rounded-lg border border-red-400/50 text-xs hover:bg-red-500/10 transition-colors"
                  >
                    Try again
                  </button>
                </div>
              </motion.div>
            )}

            {analysisResult && !loading && (
              <div className="space-y-6 relative z-10">
                <div className="flex items-center justify-between gap-3">
                  <button
                    onClick={handleReset}
                    className="text-xs text-slate-400 hover:text-slate-200 inline-flex items-center gap-1 transition-colors"
                  >
                    <span className="text-slate-500">←</span>
                    Upload another resume
                  </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  <div className="lg:col-span-2">
                    <ScoreDashboard result={analysisResult} />
                  </div>
                  <div className="lg:col-span-3">
                    <FeedbackCards result={analysisResult} />
                  </div>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Subtle footer */}
        <footer className="mt-6 flex items-center justify-between text-[11px] text-slate-500">
          <span>PDF only · All analysis happens locally on the server</span>
          <span>Built for clarity, not buzzwords</span>
        </footer>
      </div>
    </div>
  )
}

export default App