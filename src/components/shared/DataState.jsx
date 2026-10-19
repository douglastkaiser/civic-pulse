export default function DataState({ loading, error, onRetry }) {
  return (
    <div className="civic-card" role={error ? 'alert' : 'status'}>
      <p>{loading ? 'Loading your local information…' : error}</p>
      {onRetry && (
        <button className="civic-button mt-4" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  )
}
