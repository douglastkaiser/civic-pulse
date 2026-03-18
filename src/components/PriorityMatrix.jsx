import { useState, useMemo } from 'react'
import Plot from 'react-plotly.js'
import ContextTooltip from './shared/ContextTooltip'
import DetailModal from './shared/DetailModal'

const QUADRANT_COLORS = {
  act_now: '#22c55e',
  know: '#3b82f6',
  watch: '#f59e0b',
  background: '#475569',
}

function getMarkerSize(issue) {
  if (!issue.meeting_date) return 12
  const daysUntil = Math.ceil(
    (new Date(issue.meeting_date) - Date.now()) / (1000 * 60 * 60 * 24)
  )
  if (daysUntil <= 7) return 20
  if (daysUntil <= 30) return 16
  if (daysUntil <= 90) return 13
  return 10
}

function MatrixPlot({ issues, selectedIssueId, onSelectIssue }) {
  const data = useMemo(() => {
    if (!issues?.length) return []

    return [
      {
        x: issues.map((i) => i.importance_score),
        y: issues.map((i) => i.impact_score),
        text: issues.map((i) => i.title),
        customdata: issues.map((i) => i.id),
        hovertemplate:
          '<b>%{text}</b><br>Importance: %{x}<br>Impact: %{y}<extra></extra>',
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: issues.map(getMarkerSize),
          color: issues.map((i) => QUADRANT_COLORS[i.quadrant] || '#475569'),
          line: {
            color: issues.map((i) =>
              i.id === selectedIssueId ? '#e2e8f0' : 'transparent'
            ),
            width: issues.map((i) => (i.id === selectedIssueId ? 2 : 0)),
          },
          opacity: 0.85,
        },
      },
    ]
  }, [issues, selectedIssueId])

  const layout = useMemo(
    () => ({
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      margin: { t: 30, r: 20, b: 50, l: 50 },
      xaxis: {
        title: { text: 'Importance', font: { size: 11 } },
        range: [0, 100],
        gridcolor: '#1e2d4a',
        zerolinecolor: '#1e2d4a',
        color: '#64748b',
        dtick: 25,
      },
      yaxis: {
        title: { text: 'Impact', font: { size: 11 } },
        range: [0, 100],
        gridcolor: '#1e2d4a',
        zerolinecolor: '#1e2d4a',
        color: '#64748b',
        dtick: 25,
      },
      font: {
        family: 'JetBrains Mono, monospace',
        color: '#64748b',
        size: 10,
      },
      shapes: [
        {
          type: 'line',
          x0: 50, x1: 50, y0: 0, y1: 100,
          line: { color: '#1e2d4a', width: 1, dash: 'dash' },
        },
        {
          type: 'line',
          x0: 0, x1: 100, y0: 50, y1: 50,
          line: { color: '#1e2d4a', width: 1, dash: 'dash' },
        },
      ],
      annotations: [
        { x: 75, y: 95, text: 'ACT NOW', showarrow: false, font: { color: '#22c55e', size: 9 } },
        { x: 25, y: 95, text: 'KNOW', showarrow: false, font: { color: '#3b82f6', size: 9 } },
        { x: 75, y: 5, text: 'WATCH', showarrow: false, font: { color: '#f59e0b', size: 9 } },
        { x: 25, y: 5, text: 'BACKGROUND', showarrow: false, font: { color: '#475569', size: 9 } },
      ],
      dragmode: false,
      hovermode: 'closest',
    }),
    []
  )

  const config = useMemo(
    () => ({
      displayModeBar: false,
      responsive: true,
    }),
    []
  )

  const handleClick = (event) => {
    if (event.points?.[0]) {
      const issueId = event.points[0].customdata
      onSelectIssue?.(issueId)
    }
  }

  return (
    <Plot
      data={data}
      layout={layout}
      config={config}
      onClick={handleClick}
      useResizeHandler
      className="w-full h-full"
      style={{ width: '100%', height: '100%' }}
    />
  )
}

export default function PriorityMatrix({ issues, onSelectIssue, selectedIssueId }) {
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <>
      <div className="bg-bg-panel border border-border rounded-lg p-3 flex flex-col h-full panel-hover">
        <div className="flex items-center gap-2 mb-2">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            PRIORITY MATRIX
          </h2>
          <ContextTooltip text="Issues are plotted by how much they align with your stated values (importance) vs. how much leverage you have to affect the outcome (impact). Top-right quadrant items are where your time is best spent." />
          <button
            onClick={() => setModalOpen(true)}
            className="ml-auto text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-1.5 py-0.5 rounded hover:bg-bg-elevated"
            title="Expand to full view"
          >
            ⤢
          </button>
        </div>
        {issues?.length > 0 ? (
          <div className="flex-1 min-h-0">
            <MatrixPlot
              issues={issues}
              selectedIssueId={selectedIssueId}
              onSelectIssue={onSelectIssue}
            />
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="text-text-tertiary text-sm font-mono mb-2">No issues data</div>
              <div className="text-text-tertiary text-xs">
                Run the pipeline to populate issues for this location.
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Expanded modal view */}
      <DetailModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="PRIORITY MATRIX"
      >
        <div className="flex items-center gap-2 mb-4">
          <ContextTooltip text="Issues are plotted by how much they align with your stated values (importance) vs. how much leverage you have to affect the outcome (impact). Top-right quadrant items are where your time is best spent." />
        </div>
        {issues?.length > 0 ? (
          <div style={{ height: '70vh' }}>
            <MatrixPlot
              issues={issues}
              selectedIssueId={selectedIssueId}
              onSelectIssue={onSelectIssue}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-64">
            <div className="text-text-tertiary text-sm font-mono">No issues data</div>
          </div>
        )}
      </DetailModal>
    </>
  )
}
