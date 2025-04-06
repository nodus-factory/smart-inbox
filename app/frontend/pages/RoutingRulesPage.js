import React, { useState } from 'react';

const RoutingRulesPage = () => {
  // Mock data for demonstration
  const [rules, setRules] = useState([
    { 
      id: 1, 
      client_id: 1,
      client_name: 'Acme Corporation',
      classification: 'technical',
      action: 'github_issue',
      destination: 'acme/support',
      priority: 1,
      active: true
    },
    { 
      id: 2, 
      client_id: 1,
      client_name: 'Acme Corporation',
      classification: 'commercial',
      action: 'email_forward',
      destination: 'sales@internal.com',
      priority: 2,
      active: true
    },
    { 
      id: 3, 
      client_id: 2,
      client_name: 'Globex Industries',
      classification: 'technical',
      action: 'github_issue',
      destination: 'globex/helpdesk',
      priority: 1,
      active: true
    }
  ]);
  
  const clients = [
    { id: 1, name: 'Acme Corporation' },
    { id: 2, name: 'Globex Industries' },
    { id: 3, name: 'Initech' }
  ];
  
  const [showForm, setShowForm] = useState(false);
  const [currentRule, setCurrentRule] = useState(null);
  
  const handleAddNew = () => {
    setCurrentRule(null);
    setShowForm(true);
  };
  
  const handleEdit = (rule) => {
    setCurrentRule(rule);
    setShowForm(true);
  };
  
  const handleDelete = (ruleId) => {
    if (window.confirm('Are you sure you want to delete this routing rule?')) {
      setRules(rules.filter(rule => rule.id !== ruleId));
    }
  };
  
  const handleToggleActive = (ruleId) => {
    setRules(rules.map(rule => 
      rule.id === ruleId ? { ...rule, active: !rule.active } : rule
    ));
  };
  
  const handleFormSubmit = (ruleData) => {
    // Find client name for display
    const client = clients.find(c => c.id === parseInt(ruleData.client_id));
    const clientName = client ? client.name : 'Unknown Client';
    
    if (currentRule) {
      // Update existing rule
      setRules(rules.map(rule => 
        rule.id === currentRule.id ? { 
          ...rule, 
          ...ruleData,
          client_name: clientName
        } : rule
      ));
    } else {
      // Add new rule
      const newRule = {
        id: rules.length > 0 ? Math.max(...rules.map(r => r.id)) + 1 : 1,
        ...ruleData,
        client_name: clientName
      };
      setRules([...rules, newRule]);
    }
    setShowForm(false);
  };
  
  const handleFormCancel = () => {
    setShowForm(false);
  };
  
  // Import the RoutingRuleForm component
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

  return (
    <div className="routing-rules-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Routing Rules</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Rule
        </button>
      </div>
      
      {showForm ? (
        <RoutingRuleForm 
          rule={currentRule} 
          clients={clients}
          onSubmit={handleFormSubmit} 
          onCancel={handleFormCancel} 
        />
      ) : (
        <div className="card">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>Client</th>
                    <th>Classification</th>
                    <th>Action</th>
                    <th>Destination</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {rules.map(rule => (
                    <tr key={rule.id}>
                      <td>{rule.client_name}</td>
                      <td>
                        <span className={`badge ${
                          rule.classification === 'technical' ? 'badge-primary' : 
                          rule.classification === 'commercial' ? 'badge-secondary' : 
                          'badge-success'
                        }`}>
                          {rule.classification}
                        </span>
                      </td>
                      <td>{rule.action === 'github_issue' ? 'GitHub Issue' : 'Email Forward'}</td>
                      <td>{rule.destination}</td>
                      <td>{rule.priority}</td>
                      <td>
                        <div className="form-check form-switch">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            checked={rule.active}
                            onChange={() => handleToggleActive(rule.id)}
                          />
                          <label className="form-check-label">
                            {rule.active ? 'Active' : 'Inactive'}
                          </label>
                        </div>
                      </td>
                      <td>
                        <button 
                          className="btn btn-sm btn-outline mr-2" 
                          onClick={() => handleEdit(rule)}
                        >
                          Edit
                        </button>
                        <button 
                          className="btn btn-sm btn-danger" 
                          onClick={() => handleDelete(rule.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RoutingRulesPage;
