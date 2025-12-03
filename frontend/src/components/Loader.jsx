import { motion } from 'framer-motion'

function Loader() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-20 h-20">
        <motion.div
          className="absolute inset-0 rounded-full bg-gradient-to-tr from-cyan-400 via-indigo-500 to-pink-500 opacity-70 blur-sm"
          animate={{ rotate: 360 }}
          transition={{ duration: 6, repeat: Infinity, ease: 'linear' }}
        />
        <motion.div
          className="absolute inset-[3px] rounded-full bg-slate-900 border border-slate-700/80"
          initial={{ scale: 0.9, opacity: 0.4 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.4 }}
        />
        <motion.div
          className="absolute inset-[6px] rounded-full border-2 border-cyan-400/70 border-t-transparent"
          animate={{ rotate: -360 }}
          transition={{ duration: 2.2, repeat: Infinity, ease: 'linear' }}
        />
      </div>
      <p className="mt-5 text-sm font-medium text-slate-200">
        Analyzing your resume...
      </p>
      <p className="mt-1 text-xs text-slate-500">
        This usually takes just a couple of seconds.
      </p>
    </div>
  )
}

export default Loader

