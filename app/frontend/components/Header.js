import React from 'react';

const Header = () => {
  return (
    <header className="header">
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
  );
};

export default Header;
