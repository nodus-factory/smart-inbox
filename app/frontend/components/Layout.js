import React from 'react';

const Layout = ({ children }) => {
  return (
    <div className="app-layout">
      <header className="app-header">
        <div className="container">
          <div className="d-flex justify-content-between align-items-center py-3">
            <div className="logo">
              <h1>Smart Inbox</h1>
            </div>
            <nav className="main-nav">
              <ul className="d-flex">
                <li className="mx-2"><a href="/">Dashboard</a></li>
                <li className="mx-2"><a href="/clients">Clients</a></li>
                <li className="mx-2"><a href="/routing-rules">Routing Rules</a></li>
                <li className="mx-2"><a href="/emails">Emails</a></li>
                <li className="mx-2"><a href="/manual-review">Manual Review</a></li>
                <li className="mx-2"><a href="/settings">Settings</a></li>
              </ul>
            </nav>
          </div>
        </div>
      </header>
      
      <div className="app-container">
        <div className="container">
          <div className="row">
            <div className="col-md-3">
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
            </div>
            <div className="col-md-9">
              <main className="main-content p-3">
                {children}
              </main>
            </div>
          </div>
        </div>
      </div>
      
      <footer className="app-footer mt-5 py-4 bg-light">
        <div className="container">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <p className="mb-0">&copy; 2025 Smart Inbox Application</p>
            </div>
            <div>
              <a href="/privacy" className="mr-3">Privacy Policy</a>
              <a href="/terms">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
