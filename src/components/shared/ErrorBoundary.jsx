import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="h-full flex items-center justify-center p-8">
          <div className="bg-bg-panel border border-border rounded-lg p-6 max-w-md text-center">
            <div className="text-2xl mb-3">⚠</div>
            <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-2">
              SOMETHING WENT WRONG
            </h2>
            <p className="text-xs text-text-secondary mb-4">
              An unexpected error occurred. Try refreshing or navigating back.
            </p>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-4 py-1.5 text-xs font-mono text-accent-blue border border-accent-blue/30 rounded hover:bg-accent-blue/10 transition-colors"
            >
              TRY AGAIN
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
