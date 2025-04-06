import React, { useState } from 'react';

const Dashboard = () => {
  // Mock data for demonstration
  const stats = {
    totalEmails: 124,
    processedEmails: 112,
    pendingReview: 12,
    clientCount: 8,
    routingRules: 15,
    successRate: 92
  };

  const recentEmails = [
    { id: 1, sender: 'john@acmecorp.com', subject: 'API Integration Issue', classification: 'technical', status: 'processed', timestamp: '2025-04-06T06:32:10Z' },
    { id: 2, sender: 'sarah@globex.com', subject: 'Contract Renewal', classification: 'commercial', status: 'processed', timestamp: '2025-04-06T05:47:22Z' },
    { id: 3, sender: 'mike@initech.com', subject: 'Account Access Request', classification: 'administrative', status: 'pending', timestamp: '2025-04-06T05:12:45Z' },
    { id: 4, sender: 'lisa@umbrella.org', subject: 'Bug in Dashboard', classification: 'technical', status: 'processed', timestamp: '2025-04-05T22:08:33Z' },
    { id: 5, sender: 'david@wayne.com', subject: 'New Feature Request', classification: 'technical', status: 'pending', timestamp: '2025-04-05T21:15:19Z' }
  ];

  return (
    <div className="dashboard">
      <h2 className="mb-4">Dashboard</h2>
      
      <div className="stats-cards mb-5">
        <div className="row">
          <div className="col-md-4 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Email Processing</h5>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="stat-value">{stats.processedEmails}/{stats.totalEmails}</div>
                  <div className="stat-label">Processed</div>
                </div>
                <div className="progress mt-2">
                  <div 
                    className="progress-bar bg-primary" 
                    role="progressbar" 
                    style={{ width: `${(stats.processedEmails / stats.totalEmails) * 100}%` }}
                    aria-valuenow={(stats.processedEmails / stats.totalEmails) * 100}
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="col-md-4 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Pending Review</h5>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="stat-value">{stats.pendingReview}</div>
                  <div className="stat-label">Emails</div>
                </div>
                <a href="/manual-review" className="btn btn-sm btn-outline mt-3">Review Now</a>
              </div>
            </div>
          </div>
          
          <div className="col-md-4 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Success Rate</h5>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="stat-value">{stats.successRate}%</div>
                  <div className="stat-label">Accuracy</div>
                </div>
                <div className="progress mt-2">
                  <div 
                    className="progress-bar bg-success" 
                    role="progressbar" 
                    style={{ width: `${stats.successRate}%` }}
                    aria-valuenow={stats.successRate}
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="row">
          <div className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Clients</h5>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="stat-value">{stats.clientCount}</div>
                  <div className="stat-label">Total</div>
                </div>
                <a href="/clients" className="btn btn-sm btn-outline mt-3">Manage Clients</a>
              </div>
            </div>
          </div>
          
          <div className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Routing Rules</h5>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="stat-value">{stats.routingRules}</div>
                  <div className="stat-label">Active</div>
                </div>
                <a href="/routing-rules" className="btn btn-sm btn-outline mt-3">Configure Rules</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="recent-emails">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3>Recent Emails</h3>
          <a href="/emails" className="btn btn-sm btn-primary">View All</a>
        </div>
        
        <div className="card">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>Sender</th>
                    <th>Subject</th>
                    <th>Classification</th>
                    <th>Status</th>
                    <th>Time</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {recentEmails.map(email => (
                    <tr key={email.id}>
                      <td>{email.sender}</td>
                      <td>{email.subject}</td>
                      <td>
                        <span className={`badge ${
                          email.classification === 'technical' ? 'badge-primary' : 
                          email.classification === 'commercial' ? 'badge-secondary' : 
                          'badge-success'
                        }`}>
                          {email.classification}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${
                          email.status === 'processed' ? 'badge-success' : 'badge-warning'
                        }`}>
                          {email.status}
                        </span>
                      </td>
                      <td>{new Date(email.timestamp).toLocaleString()}</td>
                      <td>
                        <a href={`/emails/${email.id}`} className="btn btn-sm btn-outline">View</a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
