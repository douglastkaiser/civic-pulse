import { useState } from 'react'
import { loadAllProfiles, loadAllOrgs } from '../../lib/data'

export default function BulkExportButton() {
  const [exporting, setExporting] = useState(false)

  const handleExport = async () => {
    setExporting(true)
    try {
      const [profiles, orgs] = await Promise.all([loadAllProfiles(), loadAllOrgs()])
      const data = {
        export_type: 'bulk_all_data',
        exported_at: new Date().toISOString(),
        profiles,
        orgs,
      }
      const json = JSON.stringify(data, null, 2)
      const blob = new Blob([json], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'civic-pulse-all-data.json'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Bulk export failed:', err)
    } finally {
      setExporting(false)
    }
  }

  return (
    <button
      onClick={handleExport}
      disabled={exporting}
      className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-2 py-1 rounded border border-border hover:border-accent-blue/30 disabled:opacity-50 disabled:cursor-not-allowed"
      title="Export all profiles and orgs as JSON"
    >
      {exporting ? 'Exporting...' : 'Export All JSON'}
    </button>
  )
}
