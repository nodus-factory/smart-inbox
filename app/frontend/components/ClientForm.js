import React, { useState } from 'react';

const ClientForm = ({ client = {}, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: client.name || '',
    domains: client.domains ? client.domains.join(', ') : '',
    signature_patterns: client.signature_patterns ? client.signature_patterns.join(', ') : '',
    authorized_emails: client.authorized_emails ? client.authorized_emails.join(', ') : '',
    github_repository: client.github_repository || '',
    technical_contact: client.technical_contact || '',
    commercial_contact: client.commercial_contact || '',
    administrative_contact: client.administrative_contact || ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Process arrays from comma-separated strings
    const processedData = {
      ...formData,
      domains: formData.domains ? formData.domains.split(',').map(item => item.trim()) : [],
      signature_patterns: formData.signature_patterns ? formData.signature_patterns.split(',').map(item => item.trim()) : [],
      authorized_emails: formData.authorized_emails ? formData.authorized_emails.split(',').map(item => item.trim()) : []
    };
    
    onSubmit(processedData);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>{client.id ? 'Edit Client' : 'Add New Client'}</h3>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Client Name</label>
            <input
              type="text"
              className="form-control"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="domains">Domains (comma-separated)</label>
            <input
              type="text"
              className="form-control"
              id="domains"
              name="domains"
              value={formData.domains}
              onChange={handleChange}
              placeholder="example.com, example.org"
            />
            <small className="text-muted">Enter domain names separated by commas</small>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="signature_patterns">Signature Patterns (comma-separated)</label>
            <input
              type="text"
              className="form-control"
              id="signature_patterns"
              name="signature_patterns"
              value={formData.signature_patterns}
              onChange={handleChange}
              placeholder="Pattern 1, Pattern 2"
            />
            <small className="text-muted">Enter signature patterns separated by commas</small>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="authorized_emails">Authorized Emails (comma-separated)</label>
            <input
              type="text"
              className="form-control"
              id="authorized_emails"
              name="authorized_emails"
              value={formData.authorized_emails}
              onChange={handleChange}
              placeholder="contact@example.com, support@example.com"
            />
            <small className="text-muted">Enter authorized email addresses separated by commas</small>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="github_repository">GitHub Repository</label>
            <input
              type="text"
              className="form-control"
              id="github_repository"
              name="github_repository"
              value={formData.github_repository}
              onChange={handleChange}
              placeholder="owner/repository"
            />
            <small className="text-muted">Format: owner/repository</small>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="technical_contact">Technical Contact Email</label>
            <input
              type="email"
              className="form-control"
              id="technical_contact"
              name="technical_contact"
              value={formData.technical_contact}
              onChange={handleChange}
              placeholder="tech@internal.com"
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="commercial_contact">Commercial Contact Email</label>
            <input
              type="email"
              className="form-control"
              id="commercial_contact"
              name="commercial_contact"
              value={formData.commercial_contact}
              onChange={handleChange}
              placeholder="sales@internal.com"
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="administrative_contact">Administrative Contact Email</label>
            <input
              type="email"
              className="form-control"
              id="administrative_contact"
              name="administrative_contact"
              value={formData.administrative_contact}
              onChange={handleChange}
              placeholder="admin@internal.com"
            />
          </div>
          
          <div className="d-flex justify-content-between mt-4">
            <button type="button" className="btn btn-outline" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {client.id ? 'Update Client' : 'Add Client'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ClientForm;
