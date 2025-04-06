import React, { useState } from 'react';

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
              <div className="col-md-10">{email.received_at || new Date().toLocaleString()}</div>
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

export default ManualReviewInterface;
