import pandas as pd

def read_company_list(file_path):
    """Read company list from an Excel file."""
    return pd.read_excel(file_path)

def export_contact_results(contact_data, output_path):
    """Export contact results to an Excel file."""
    df = pd.DataFrame(contact_data)
    df.to_excel(output_path, index=False)