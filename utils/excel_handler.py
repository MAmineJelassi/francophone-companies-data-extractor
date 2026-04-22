import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment


class ExcelHandler:
    def read_companies(self, filepath):
        """Read company names from column A of an Excel file."""
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        companies = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                companies.append(str(row[0]).strip())
        return companies

    def write_results(self, filepath, results):
        """Write extracted contact results to an Excel file."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Results'

        if not results:
            wb.save(filepath)
            return

        headers = list(results[0].keys())

        # Write header row with styling
        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True)
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        # Write data rows
        for row_idx, record in enumerate(results, 2):
            for col_idx, key in enumerate(headers, 1):
                ws.cell(row=row_idx, column=col_idx, value=record.get(key, 'N/A'))

        # Auto-size columns
        for col in ws.columns:
            max_length = max((len(str(cell.value)) for cell in col if cell.value), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(max_length + 4, 60)

        wb.save(filepath)
