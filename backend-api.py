# Logic for backend to first check the hot container and then the cold container.

def get_billing_record(record_id):
    # First, check in Billing_Recent
    record = recent_container.read_item(record_id, partition_key)
    if record:
        return record

    # If not found, fallback to Billing_Archive
    record = archive_container.read_item(record_id, partition_key)
    if record:
        return record

    return "Record not found"
