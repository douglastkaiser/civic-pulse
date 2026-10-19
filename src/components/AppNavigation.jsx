import { NavLink, Link } from 'react-router-dom'
import { useAuth } from '../lib/auth'
export default function AppNavigation() {
  const { user, signOut } = useAuth()
  const items = [
    [user ? '/dashboard' : '/', 'Home'],
    ['/explore', 'Explore'],
    ...(!user
      ? [['/demo', 'Example briefing']]
      : [
          ['/saved', 'Saved'],
          ['/organizations', 'Organizations'],
          ['/settings', 'Profile'],
        ]),
  ]
  return (
    <header className="app-menu">
      <Link className="app-wordmark" to={user ? '/dashboard' : '/demo'}>
        CIVIC PULSE<span>LOCAL CIVIC DESK</span>
      </Link>
      <nav aria-label="Main navigation" className="desk-navigation">
        {items.map(([path, name]) => (
          <NavLink
            key={path}
            to={path}
            end={path === '/'}
            className={({ isActive }) =>
              `desk-link ${isActive ? 'desk-link-active' : ''}`
            }
          >
            {name}
          </NavLink>
        ))}
      </nav>
      <div className="desk-reference">
        <span className="menu-caption">REFERENCE</span>
        <Link to="/officials/austin-78702">Officials</Link>
        <Link to="/elections/austin-78702">Elections</Link>
      </div>
      <nav className="desk-preferences" aria-label="Preferences">
        <NavLink
          to="/appearance"
          className={({ isActive }) =>
            `desk-link ${isActive ? 'desk-link-active' : ''}`
          }
        >
          Appearance
        </NavLink>
        {user ? (
          <button className="desk-link" onClick={signOut}>
            Sign out
          </button>
        ) : (
          <Link className="desk-link" to="/signin">
            Sign in
          </Link>
        )}
      </nav>
    </header>
  )
}
