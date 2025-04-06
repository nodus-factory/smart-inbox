import React, { useState } from 'react';

const ManualReviewPage = () => {
  // Mock data for demonstration
  const [pendingEmails, setPendingEmails] = useState([
    { 
      id: 1, 
      sender: 'mike@initech.com', 
      recipient: 'inbox@smartinbox.com',
      subject: 'Account Access Request', 
      body: 'Hello, I need access to our company account. Can you please help me with this process?',
      received_at: '2025-04-06T05:12:45Z',
      classification: 'administrative',
      confidence_score: 0.65
    },
    { 
      id: 2, 
      sender: 'david@wayne.com', 
      recipient: 'inbox@smartinbox.com',
      subject: 'New Feature Request', 
      body: 'We would like to request a new feature for our dashboard that shows real-time analytics.',
      received_at: '2025-04-05T21:15:19Z',
      classification: 'technical',
      confidence_score: 0.68
    },
    { 
      id: 3, 
      sender: 'sarah@globex.com', 
      recipient: 'inbox@smartinbox.com',
      subject: 'Meeting Request', 
      body: 'I would like to schedule a meeting to discuss our ongoing project and next steps.',
      received_at: '2025-04-05T18:22:37Z',
      classification: 'administrative',
      confidence_score: 0.62
    }
  ]);
  
  const clients = [
    { id: 1, name: 'Acme Corporation' },
    { id: 2, name: 'Globex Industries' },
    { id: 3, name: 'Initech' },
    { id: 4, name: 'Wayne Enterprises' }
  ];
  
  const [currentEmail, setCurrentEmail] = useState(null);
  
  const handleSelectEmail = (email) => {
    setCurrentEmail(email);
  };
  
  const handleApprove = (data) => {
    console.log('Approved email with data:', data);
    // In a real application, this would call an API to process the email
    setPendingEmails(pendingEmails.filter(email => email.id !== data.email_id));
    setCurrentEmail(null);
  };
  
  const handleReject = (data) => {
    console.log('Rejected email with data:', data);
    // In a real application, this would call an API to delete or archive the email
    setPendingEmails(pendingEmails.filter(email => email.id !== data.email_id));
    setCurrentEmail(null);
  };
  
  // Import the ManualReviewInterface component
  const ManualReviewInterface = ({ email = {}, clients = [], onApprove, onReject }) => {
    const [classification, setClassification] = useState(email.classification || 'technical');
    const [selectedClient, setSelectedClient] = useState(email.client_id || '');
    const [notes, setNotes] = useState('');

    const handleApprove = () => {
      onApprove({
        email_id: email.id,
        classification,
        client_id: selectedClient,
        notes
      });
    };

    const handleReject = () => {
      onReject({
        email_id: email.id,
        notes
      });
    };

    return (
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h3>Manual Review</h3>
          <span className="badge badge-warning">Pending Review</span>
        </div>
        <div className="card-body">
          <div className="email-details mb-4">
            <h4>Email Details</h4>
            <div className="email-header p-3 bg-light rounded mb-3">
              <div className="row mb-2">
                <div className="col-md-2 font-weight-bold">From:</div>
                <div className="col-md-10">{email.sender || 'example@client.com'}</div>
              </div>
              <div className="row mb-2">
                <div className="col-md-2 font-weight-bold">To:</div>
                <div className="col-md-10">{email.recipient || 'inbox@smartinbox.com'}</div>
              </div>
              <div className="row mb-2">
                <div className="col-md-2 font-weight-bold">Subject:</div>
                <div className="col-md-10">{email.subject || 'Example Subject Line'}</div>
              </div>
              <div className="row mb-2">
                <div className="col-md-2 font-weight-bold">Date:</div>
                <div className="col-md-10">{email.received_at ? new Date(email.received_at).toLocaleString() : new Date().toLocaleString()}</div>
              </div>
            </div>
            
            <div className="email-body p-3 border rounded mb-3">
              <h5>Email Content</h5>
              <p>{email.body || 'This is an example email body content that needs manual review. The AI classification system was not confident enough to automatically route this email.'}</p>
              
              {email.attachments && email.attachments.length > 0 && (
                <div className="email-attachments mt-3">
                  <h6>Attachments</h6>
                  <ul>
                    {email.attachments.map((attachment, index) => (
                      <li key={index}>{attachment}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
          
          <div className="review-form">
            <h4>Review Decision</h4>
            
            <div className="form-group">
              <label className="form-label" htmlFor="client">Client</label>
              <select
                className="form-select"
                id="client"
                value={selectedClient}
                onChange={(e) => setSelectedClient(e.target.value)}
                required
              >
                <option value="">Select a client</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>{client.name}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label className="form-label">Classification</label>
              <div className="d-flex">
                <div className="form-check mr-3">
                  <input
                    type="radio"
                    className="form-check-input"
                    id="technical"
                    name="classification"
                    value="technical"
                    checked={classification === 'technical'}
                    onChange={() => setClassification('technical')}
                  />
                  <label className="form-check-label" htmlFor="technical">Technical</label>
                </div>
                <div className="form-check mr-3">
                  <input
                    type="radio"
                    className="form-check-input"
                    id="commercial"
                    name="classification"
                    value="commercial"
                    checked={classification === 'commercial'}
                    onChange={() => setClassification('commercial')}
                  />
                  <label className="form-check-label" htmlFor="commercial">Commercial</label>
                </div>
                <div className="form-check">
                  <input
                    type="radio"
                    className="form-check-input"
                    id="administrative"
                    name="classification"
                    value="administrative"
                    checked={classification === 'administrative'}
                    onChange={() => setClassification('administrative')}
                  />
                  <label className="form-check-label" htmlFor="administrative">Administrative</label>
                </div>
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label" htmlFor="notes">Notes</label>
              <textarea
                className="form-control"
                id="notes"
                rows="3"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Add any notes about this decision..."
              ></textarea>
            </div>
            
            <div className="d-flex justify-content-between mt-4">
              <button type="button" className="btn btn-danger" onClick={handleReject}>
                Reject / Delete
              </button>
              <button type="button" className="btn btn-primary" onClick={handleApprove} disabled={!selectedClient}>
                Approve & Route
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="manual-review-page">
      <h2 className="mb-4">Manual Review</h2>
      
      <div className="row">
        {currentEmail ? (
          <div className="col-12">
            <ManualReviewInterface 
              email={currentEmail} 
              clients={clients}
              onApprove={handleApprove}
              onReject={handleReject}
            />
          </div>
        ) : (
          <>
            <div className="col-12 mb-4">
              <div className="alert alert-info">
                <p className="mb-0">
                  <strong>Manual Review Queue:</strong> {pendingEmails.length} emails pending review
                </p>
              </div>
            </div>
            
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h3>Pending Emails</h3>
                </div>
                <div className="card-body p-0">
                  {pendingEmails.length === 0 ? (
                    <div className="p-4 text-center">
                      <p>No emails pending review.</p>
                    </div>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-hover mb-0">
                        <thead>
                          <tr>
                            <th>Sender</th>
                            <th>Subject</th>
                            <th>Received</th>
                            <th>AI Classification</th>
                            <th>Confidence</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {pendingEmails.map(email => (
                            <tr key={email.id}>
                              <td>{email.sender}</td>
                              <td>{email.subject}</td>
                              <td>{new Date(email.received_at).toLocaleString()}</td>
                              <td>
                                <span className={`badge ${
                                  email.classification === 'technical' ? 'badge-primary' : 
                                  email.classification === 'commercial' ? 'badge-secondary' : 
                                  'badge-success'
                                }`}>
                                  {email.classification}
                                </span>
                              </td>
                              <td>{(email.confidence_score * 100).toFixed(0)}%</td>
                              <td>
                                <button 
                                  className="btn btn-sm btn-primary" 
                                  onClick={() => handleSelectEmail(email)}
                                >
                                  Review
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ManualReviewPage;
