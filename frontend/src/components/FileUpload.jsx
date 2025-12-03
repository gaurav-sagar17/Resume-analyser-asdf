import { useRef, useState } from 'react'

function FileUpload({ onFileUpload, error }) {
  const fileInputRef = useRef(null)
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        onFileUpload(file)
      } else {
        alert('Please upload a PDF file')
      }
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        onFileUpload(file)
      } else {
        alert('Please upload a PDF file')
      }
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="w-full space-y-4">
      <div
        className={`relative border rounded-2xl p-8 md:p-10 transition-all cursor-pointer
        ${dragActive
            ? 'border-cyan-400/80 bg-cyan-500/5 shadow-[0_0_35px_rgba(34,211,238,0.25)]'
            : 'border-slate-700/80 bg-slate-900/60 hover:border-cyan-400/60 hover:bg-slate-900/80'
          }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
        />

        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="relative">
            <div className="h-16 w-16 rounded-2xl bg-slate-800/80 border border-slate-600 flex items-center justify-center">
              <span className="h-7 w-7 rounded-lg bg-cyan-400/20 border border-cyan-400/60 flex items-center justify-center">
                <span className="h-2.5 w-2.5 rounded-sm bg-cyan-400 shadow-[0_0_18px_rgba(34,211,238,0.9)]" />
              </span>
            </div>
            <div className="absolute -bottom-1 -right-1 h-4 w-4 rounded-full bg-emerald-400/90 shadow-[0_0_15px_rgba(52,211,153,0.9)]" />
          </div>

          <div className="flex-1 text-left space-y-2">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-500">
              Upload PDF
            </p>
            <p className="text-lg md:text-xl font-medium text-slate-50">
              {selectedFile ? selectedFile.name : 'Drop your resume here or browse'}
            </p>
            <p className="text-xs md:text-sm text-slate-400">
              We only read the text from your PDF. No files are stored.
            </p>
          </div>

          <button
            type="button"
            className="px-5 py-2.5 rounded-xl bg-cyan-500 text-slate-900 text-sm font-medium
            hover:bg-cyan-400 transition-colors shadow-[0_10px_30px_rgba(34,211,238,0.45)]"
          >
            Choose PDF
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/40 text-red-200 px-4 py-3 rounded-xl text-xs">
          <p className="font-medium mb-1">Upload error</p>
          <p className="opacity-90">{error}</p>
        </div>
      )}
    </div>
  )
}

export default FileUpload