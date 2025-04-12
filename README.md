# billing-cost-optimization
Optimize Cosmos DB billing data costs


To optimize the cost of storing billing records in Azure Cosmos DB, we can implement a hot/cold data separation strategy within Cosmos DB itself, without the need to archive data outside the platform.

## How It Works

### Two Containers
Billing records are split into two logical containers:
- **`Billing_Recent`**: Holds new and frequently accessed data (last 6 months).
- **`Billing_Archive`**: Holds older, rarely accessed data (older than 6 months).

### Automated Archiving
A lightweight Azure Function runs daily:

1. Queries `Billing_Recent` for records older than 6 months using a timestamp filter.
2. Inserts those records into `Billing_Archive`.
3. Deletes them from `Billing_Recent` after successful migration.

### Transparent Access
The backend handles record retrieval logic:
- First, it checks `Billing_Recent`.
- If not found, it queries `Billing_Archive`.
- This logic is abstracted from the client — the API behavior remains unchanged.

## Benefits
- **Improved Performance**:  
  `Billing_Recent` remains lean and fast, with higher RU/s provisioned to support frequent access.

- **Cost Savings**:  
  `Billing_Archive` is configured with lower RU/s since it’s rarely queried — reducing ongoing cost.

- **Full Cosmos DB Capabilities**:  
  Both containers remain in Cosmos DB, so you retain:
  - Indexing
  - Querying
  - No need for external storage or syncing