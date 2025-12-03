import { motion } from 'framer-motion'
import { BadgeCheck, AlertTriangle, LayoutPanelLeft } from 'lucide-react'

function FeedbackCards({ result }) {
  const { strengths, weaknesses, detected_sections, field } = result

  const listVariants = {
    hidden: { opacity: 0, y: 4 },
    visible: (i) => ({
      opacity: 1,
      y: 0,
      transition: { delay: 0.03 * i, duration: 0.2 },
    }),
  }

  const prettyField =
    field && field.length > 0
      ? field.charAt(0).toUpperCase() + field.slice(1)
      : null

  return (
    <div className="space-y-4">
      {/* Field & sections card */}
      <motion.div
        className="rounded-2xl bg-slate-900/70 border border-slate-700/70 p-4 space-y-4"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <LayoutPanelLeft className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-medium uppercase tracking-[0.18em] text-slate-400">
                Structure
              </span>
            </div>
            <p className="text-sm text-slate-200">
              We scan your resume for key sections and try to infer your primary field.
            </p>
          </div>
          {prettyField && (
            <div className="px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-400/40 text-[11px] text-cyan-200 whitespace-nowrap">
              Detected field: <span className="font-medium ml-1">{prettyField}</span>
            </div>
          )}
        </div>

        <div className="flex flex-wrap gap-1.5">
          {Object.entries(detected_sections).map(([section, active], idx) => (
            <motion.span
              key={section}
              className={`px-2.5 py-1 rounded-full text-[11px] border ${
                active
                  ? 'bg-emerald-500/10 border-emerald-400/40 text-emerald-200'
                  : 'bg-slate-900/80 border-slate-700 text-slate-500'
              }`}
              custom={idx}
              variants={listVariants}
              initial="hidden"
              animate="visible"
            >
              {section} {active ? '•' : '×'}
            </motion.span>
          ))}
        </div>
      </motion.div>

      {/* Strengths */}
      {strengths.length > 0 && (
        <motion.div
          className="rounded-2xl bg-emerald-500/5 border border-emerald-400/40 p-5 space-y-3"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.05 }}
        >
          <div className="flex items-center gap-2 mb-1">
            <BadgeCheck className="w-4 h-4 text-emerald-300" />
            <h3 className="text-sm font-semibold text-emerald-100 uppercase tracking-[0.16em]">
              Strengths
            </h3>
          </div>
          <ul className="space-y-1.5">
            {strengths.map((strength, index) => (
              <motion.li
                key={index}
                className="flex items-start text-xs text-emerald-100/90"
                custom={index}
                variants={listVariants}
                initial="hidden"
                animate="visible"
              >
                <span className="mt-0.5 mr-2 h-1.5 w-1.5 rounded-full bg-emerald-300" />
                <span>{strength}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* Weaknesses */}
      {weaknesses.length > 0 && (
        <motion.div
          className="rounded-2xl bg-amber-500/5 border border-amber-400/40 p-5 space-y-3"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.08 }}
        >
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle className="w-4 h-4 text-amber-300" />
            <h3 className="text-sm font-semibold text-amber-100 uppercase tracking-[0.16em]">
              Areas for improvement
            </h3>
          </div>
          <ul className="space-y-1.5">
            {weaknesses.map((weakness, index) => (
              <motion.li
                key={index}
                className="flex items-start text-xs text-amber-100/90"
                custom={index}
                variants={listVariants}
                initial="hidden"
                animate="visible"
              >
                <span className="mt-0.5 mr-2 h-1.5 w-1.5 rounded-full bg-amber-300" />
                <span>{weakness}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>
      )}

      {strengths.length === 0 && weaknesses.length === 0 && (
        <motion.div
          className="rounded-2xl bg-slate-900/70 border border-slate-700/70 p-5 text-center text-xs text-slate-400"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          No specific feedback available for this resume.
        </motion.div>
      )}
    </div>
  )
}

export default FeedbackCards

