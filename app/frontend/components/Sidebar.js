import React from 'react';

const Sidebar = () => {
  return (
    <aside className="sidebar bg-light p-3">
      <div className="sidebar-header mb-4">
        <h4>Navigation</h4>
      </div>
      <div className="sidebar-content">
        <ul className="sidebar-nav">
          <li className="sidebar-item mb-2">
            <a href="/" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">📊</span>
              <span>Dashboard</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/clients" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">👥</span>
              <span>Clients</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/routing-rules" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">🔄</span>
              <span>Routing Rules</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/emails" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">✉️</span>
              <span>Emails</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/manual-review" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">👁️</span>
              <span>Manual Review</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/logs" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">📝</span>
              <span>Logs</span>
            </a>
          </li>
          <li className="sidebar-item mb-2">
            <a href="/settings" className="sidebar-link d-flex align-items-center">
              <span className="icon mr-2">⚙️</span>
              <span>Settings</span>
            </a>
          </li>
        </ul>
      </div>
      <div className="sidebar-footer mt-5">
        <div className="system-status p-2 bg-success text-white rounded">
          <small>System Status: Online</small>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
