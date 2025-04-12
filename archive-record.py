# Pseudocode for archiving the records.

def move_old_records():
    recent_container = cosmos_client.get_container("Billing_Recent")
    archive_container = cosmos_client.get_container("Billing_Archive")

    # Define timestamp threshold (6 months ago)
    cutoff_date = get_current_date() - timedelta(days=180)

    # Query old records
    old_records = recent_container.query_items(
        f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date}'"
    )

    for record in old_records:
        archive_container.create_item(body=record)    # Insert to archive
        recent_container.delete_item(record['id'], partition_key=record['userId'])  # Remove from recent
