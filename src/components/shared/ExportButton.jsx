export default function ExportButton({ getData, filename }) {
  const handleExport = () => {
    const data = getData()
    const json = JSON.stringify(data, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <button
      onClick={handleExport}
      className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-2 py-1 rounded border border-border hover:border-accent-blue/30"
      title="Export political metadata as JSON"
    >
      Export JSON
    </button>
  )
}
