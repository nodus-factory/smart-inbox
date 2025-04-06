import React, { useState } from 'react';

const RoutingRuleForm = ({ rule = {}, clients = [], onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    client_id: rule.client_id || '',
    classification: rule.classification || 'technical',
    action: rule.action || 'github_issue',
    destination: rule.destination || '',
    priority: rule.priority || 1,
    active: rule.active !== undefined ? rule.active : true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3>{rule.id ? 'Edit Routing Rule' : 'Add New Routing Rule'}</h3>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="client_id">Client</label>
            <select
              className="form-select"
              id="client_id"
              name="client_id"
              value={formData.client_id}
              onChange={handleChange}
              required
            >
              <option value="">Select a client</option>
              {clients.map(client => (
                <option key={client.id} value={client.id}>{client.name}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="classification">Classification</label>
            <select
              className="form-select"
              id="classification"
              name="classification"
              value={formData.classification}
              onChange={handleChange}
              required
            >
              <option value="technical">Technical</option>
              <option value="commercial">Commercial</option>
              <option value="administrative">Administrative</option>
            </select>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="action">Action</label>
            <select
              className="form-select"
              id="action"
              name="action"
              value={formData.action}
              onChange={handleChange}
              required
            >
              <option value="github_issue">Create GitHub Issue</option>
              <option value="email_forward">Forward Email</option>
            </select>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="destination">
              {formData.action === 'github_issue' ? 'GitHub Repository' : 'Email Address'}
            </label>
            <input
              type={formData.action === 'email_forward' ? 'email' : 'text'}
              className="form-control"
              id="destination"
              name="destination"
              value={formData.destination}
              onChange={handleChange}
              placeholder={formData.action === 'github_issue' ? 'owner/repository' : 'email@internal.com'}
              required
            />
            <small className="text-muted">
              {formData.action === 'github_issue' 
                ? 'Format: owner/repository' 
                : 'Email address to forward to'}
            </small>
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="priority">Priority</label>
            <input
              type="number"
              className="form-control"
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              min="1"
              max="100"
              required
            />
            <small className="text-muted">Higher number means higher priority</small>
          </div>
          
          <div className="form-group">
            <div className="form-check">
              <input
                type="checkbox"
                className="form-check-input"
                id="active"
                name="active"
                checked={formData.active}
                onChange={handleChange}
              />
              <label className="form-check-label" htmlFor="active">Active</label>
            </div>
          </div>
          
          <div className="d-flex justify-content-between mt-4">
            <button type="button" className="btn btn-outline" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {rule.id ? 'Update Rule' : 'Add Rule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RoutingRuleForm;
