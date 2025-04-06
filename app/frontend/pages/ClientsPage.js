import React, { useState } from 'react';

const ClientsPage = () => {
  // Mock data for demonstration
  const [clients, setClients] = useState([
    { 
      id: 1, 
      name: 'Acme Corporation', 
      domains: ['acmecorp.com', 'acme-inc.org'],
      github_repository: 'acme/support',
      technical_contact: 'tech@internal.com',
      commercial_contact: 'sales@internal.com',
      administrative_contact: 'admin@internal.com'
    },
    { 
      id: 2, 
      name: 'Globex Industries', 
      domains: ['globex.com'],
      github_repository: 'globex/helpdesk',
      technical_contact: 'tech@internal.com',
      commercial_contact: 'sales@internal.com',
      administrative_contact: 'admin@internal.com'
    },
    { 
      id: 3, 
      name: 'Initech', 
      domains: ['initech.com'],
      github_repository: 'initech/support',
      technical_contact: 'tech@internal.com',
      commercial_contact: 'sales@internal.com',
      administrative_contact: 'admin@internal.com'
    }
  ]);
  
  const [showForm, setShowForm] = useState(false);
  const [currentClient, setCurrentClient] = useState(null);
  
  const handleAddNew = () => {
    setCurrentClient(null);
    setShowForm(true);
  };
  
  const handleEdit = (client) => {
    setCurrentClient(client);
    setShowForm(true);
  };
  
  const handleDelete = (clientId) => {
    if (window.confirm('Are you sure you want to delete this client?')) {
      setClients(clients.filter(client => client.id !== clientId));
    }
  };
  
  const handleFormSubmit = (clientData) => {
    if (currentClient) {
      // Update existing client
      setClients(clients.map(client => 
        client.id === currentClient.id ? { ...client, ...clientData } : client
      ));
    } else {
      // Add new client
      const newClient = {
        id: clients.length > 0 ? Math.max(...clients.map(c => c.id)) + 1 : 1,
        ...clientData
      };
      setClients([...clients, newClient]);
    }
    setShowForm(false);
  };
  
  const handleFormCancel = () => {
    setShowForm(false);
  };
  
  // Import the ClientForm component
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

  return (
    <div className="clients-page">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Clients</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Client
        </button>
      </div>
      
      {showForm ? (
        <ClientForm 
          client={currentClient} 
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
                    <th>Name</th>
                    <th>Domains</th>
                    <th>GitHub Repository</th>
                    <th>Technical Contact</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {clients.map(client => (
                    <tr key={client.id}>
                      <td>{client.name}</td>
                      <td>
                        {client.domains && client.domains.map((domain, index) => (
                          <span key={index} className="badge badge-light mr-1">{domain}</span>
                        ))}
                      </td>
                      <td>{client.github_repository}</td>
                      <td>{client.technical_contact}</td>
                      <td>
                        <button 
                          className="btn btn-sm btn-outline mr-2" 
                          onClick={() => handleEdit(client)}
                        >
                          Edit
                        </button>
                        <button 
                          className="btn btn-sm btn-danger" 
                          onClick={() => handleDelete(client.id)}
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

export default ClientsPage;
