import pandas as pd


class ExcelHandler:
    """Handles reading and writing Excel files for the automation agent."""

    def read_companies(self, file_path):
        """Read company names from an Excel file.

        Expects the file to have a 'Company Name' column.
        Returns a list of company name strings.
        """
        df = pd.read_excel(file_path)
        if 'Company Name' in df.columns:
            return df['Company Name'].dropna().tolist()
        # Fallback: use the first column if 'Company Name' is not found
        return df.iloc[:, 0].dropna().tolist()

    def write_results(self, file_path, results):
        """Write contact extraction results to an Excel file.

        Args:
            file_path: Path where the output Excel file will be saved.
            results: List of dicts containing contact data.
        """
        df = pd.DataFrame(results)
        df.to_excel(file_path, index=False)


# Standalone helper functions kept for backwards compatibility
def read_company_list(file_path):
    """Read company list from an Excel file."""
    return pd.read_excel(file_path)


def export_contact_results(contact_data, output_path):
    """Export contact results to an Excel file."""
    df = pd.DataFrame(contact_data)
    df.to_excel(output_path, index=False)