import { motion } from 'framer-motion'
import { Gauge, Sparkles, ShieldCheck } from 'lucide-react'

function ScoreDashboard({ result }) {
  const { score, sections, ats_readiness } = result

  const sectionMaxScores = {
    skills: 2,
    experience: 3,
    education: 1,
    projects: 2,
    formatting: 2,
  }

  const normalized = Math.min(Math.max(score / 10, 0), 1)

  return (
    <div className="space-y-6">
      {/* Overall Score + ATS badge */}
      <motion.div
        className="relative flex flex-col items-center justify-center p-4 rounded-3xl bg-slate-900/70 border border-slate-700/70 shadow-glass-xl overflow-hidden"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="absolute inset-0 pointer-events-none opacity-40">
          <div className="absolute -top-20 -right-10 h-40 w-40 bg-ring-gradient rounded-full blur-3xl" />
          <div className="absolute -bottom-20 -left-10 h-32 w-32 bg-cyan-500/40 rounded-full blur-3xl" />
        </div>

        <div className="relative flex items-center justify-between w-full mb-3">
          <div className="flex items-center gap-2 text-slate-200 text-sm">
            <Gauge className="w-4 h-4 text-cyan-400" />
            Overall score
          </div>
          <div className="flex items-center gap-2">
            {typeof ats_readiness === 'number' && (
              <div className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-500/10 border border-emerald-400/40 text-[10px] text-emerald-100">
                <ShieldCheck className="w-3 h-3 text-emerald-300" />
                <span className="uppercase tracking-[0.16em]">
                  ATS {Math.round(ats_readiness)}%
                </span>
              </div>
            )}
            <div className="flex items-center gap-1 text-[11px] uppercase tracking-[0.16em] text-slate-400">
              <Sparkles className="w-3 h-3 text-amber-300" />
              Rule-based
            </div>
          </div>
        </div>

        <div className="relative flex items-center justify-center my-2">
          <motion.div
            className="h-36 w-36 rounded-full bg-slate-900/80 border border-slate-700/70 flex items-center justify-center"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.35 }}
          >
            <motion.div
              className="absolute inset-[3px] rounded-full border border-slate-600/60"
              style={{
                backgroundImage:
                  'radial-gradient(circle at 30% 0, rgba(56,189,248,0.35), transparent 55%), radial-gradient(circle at 70% 100%, rgba(129,140,248,0.25), transparent 55%)',
              }}
            />
            <motion.div
              className="absolute inset-[6px] rounded-full border-2 border-cyan-400/70 border-t-transparent border-r-transparent"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 4.5, ease: 'linear' }}
              style={{ boxShadow: '0 0 25px rgba(34,211,238,0.55)' }}
            />
            <div className="relative z-10 text-center">
              <div className="text-4xl font-semibold text-slate-50 tracking-tight">
                {score.toFixed(1)}
              </div>
              <div className="text-[11px] uppercase tracking-[0.18em] text-slate-400 mt-1">
                / 10
              </div>
            </div>
          </motion.div>
        </div>

        <div className="relative z-10 mt-3 flex items-center justify-center gap-3 text-[11px] text-slate-400">
          <span className="inline-flex items-center gap-1">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            Strong
          </span>
          <span className="inline-flex items-center gap-1">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
            Solid
          </span>
          <span className="inline-flex items-center gap-1">
            <span className="h-1.5 w-1.5 rounded-full bg-rose-400" />
            Needs work
          </span>
        </div>
      </motion.div>

      {/* Section Scores */}
      <motion.div
        className="rounded-2xl bg-slate-900/70 border border-slate-700/70 p-4 space-y-3"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.05 }}
      >
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium uppercase tracking-[0.18em] text-slate-400">
            Section breakdown
          </span>
          <span className="text-[11px] text-slate-500">Weighted to 10.0</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {Object.entries(sections).map(([section, sectionScore], index) => {
            const maxScore = sectionMaxScores[section]
            const percentage = (sectionScore / maxScore) * 100

            let barColor = 'from-rose-500 to-orange-400'
            if (percentage >= 80) barColor = 'from-emerald-400 to-cyan-400'
            else if (percentage >= 60) barColor = 'from-amber-400 to-yellow-300'

            return (
              <motion.div
                key={section}
                className="rounded-xl bg-slate-900/60 border border-slate-700/70 p-3"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35, delay: 0.05 * (index + 1) }}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-medium text-slate-200 capitalize">
                    {section}
                  </span>
                  <span className="text-[11px] text-slate-400">
                    {sectionScore.toFixed(1)} / {maxScore}
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                  <motion.div
                    className={`h-full rounded-full bg-gradient-to-r ${barColor}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: 0.7, delay: 0.05 * (index + 1) }}
                  />
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}

export default ScoreDashboard

