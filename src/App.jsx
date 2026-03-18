import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import PersonalDashboard from './components/PersonalDashboard'
import OrgDashboard from './components/OrgDashboard'
import OrgPublicView from './components/OrgPublicView'
import NewOrg from './components/NewOrg'

export default function App() {
  const location = useLocation()
  const isPublicView = location.pathname.endsWith('/public')

  // Public view renders without sidebar
  if (isPublicView) {
    return (
      <Routes>
        <Route path="/org/:orgId/public" element={<OrgPublicView />} />
      </Routes>
    )
  }

  return (
    <div className="h-screen bg-bg-primary flex overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-hidden">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<PersonalDashboard />} />
          <Route path="/org/new" element={<NewOrg />} />
          <Route path="/org/:orgId/public" element={<OrgPublicView />} />
          <Route path="/org/:orgId" element={<OrgDashboard />} />
        </Routes>
      </main>
    </div>
  )
}
