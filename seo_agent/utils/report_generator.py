from typing import Dict, List, Any, Optional
import json
import os
import csv
from datetime import datetime


class ReportGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.reports_folder = config.get("output", {}).get(
            "reports_folder", "./data/exports"
        )
        self.auto_timestamp = config.get("output", {}).get("auto_timestamp", True)

    def _generate_filename(self, base_name: str, extension: str) -> str:
        """Generate a filename with optional timestamp"""
        if self.auto_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{base_name}_{timestamp}.{extension}"
        else:
            return f"{base_name}.{extension}"

    def _ensure_reports_folder(self) -> None:
        """Ensure the reports folder exists"""
        os.makedirs(self.reports_folder, exist_ok=True)

    def save_json(self, data: Dict[str, Any], base_name: str) -> str:
        """Save data as JSON"""
        self._ensure_reports_folder()
        filename = self._generate_filename(base_name, "json")
        file_path = os.path.join(self.reports_folder, filename)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return file_path

    def save_csv(
        self,
        data: List[Dict[str, Any]],
        base_name: str,
        fieldnames: Optional[List[str]] = None,
    ) -> str:
        """Save data as CSV"""
        self._ensure_reports_folder()
        filename = self._generate_filename(base_name, "csv")
        file_path = os.path.join(self.reports_folder, filename)

        # Determine fieldnames if not provided and ensure not None
        field_names_to_use: List[str] = []
        if not fieldnames and data:
            field_names_to_use = list(data[0].keys())
        elif fieldnames is not None:
            field_names_to_use = fieldnames

        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field_names_to_use)
            writer.writeheader()
            writer.writerows(data)

        return file_path

    def save_html(self, html_content: str, base_name: str) -> str:
        """Save HTML report"""
        self._ensure_reports_folder()
        filename = self._generate_filename(base_name, "html")
        file_path = os.path.join(self.reports_folder, filename)

        with open(file_path, "w") as f:
            f.write(html_content)

        return file_path

    def save_markdown(self, markdown_content: str, base_name: str) -> str:
        """Save Markdown report"""
        self._ensure_reports_folder()
        filename = self._generate_filename(base_name, "md")
        file_path = os.path.join(self.reports_folder, filename)

        with open(file_path, "w") as f:
            f.write(markdown_content)

        return file_path

    def generate_keyword_report_html(self, keyword_data: Dict[str, Any]) -> str:
        """Generate HTML report for keyword research"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Keyword Research Report - {keyword_data.get('seed_keyword', 'Keywords')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .section {{ margin: 20px 0; }}
                .intent-group {{ margin: 10px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Keyword Research Report</h1>
            <div class="section">
                <h2>Overview</h2>
                <p><strong>Seed Keyword:</strong> {keyword_data.get('seed_keyword', 'N/A')}</p>
                <p><strong>Industry:</strong> {keyword_data.get('industry', 'N/A')}</p>
                <p><strong>Total Keywords:</strong> {keyword_data.get('total_keywords', 0)}</p>
            </div>

            <div class="section">
                <h2>Keywords by Search Intent</h2>
        """

        # Add intent groups
        for intent, keywords in keyword_data.get("intent_groups", {}).items():
            html += f"""
                <div class="intent-group">
                    <h3>{intent.capitalize()} Intent</h3>
                    <ul>
            """

            for keyword in keywords:
                html += f"<li>{keyword}</li>\n"

            html += """
                    </ul>
                </div>
            """

        # Add keyword table
        html += """
            <div class="section">
                <h2>All Keywords</h2>
                <table>
                    <tr>
                        <th>Keyword</th>
                        <th>Search Intent</th>
                        <th>Competition</th>
                    </tr>
        """

        for kw in keyword_data.get("keywords", []):
            html += f"""
                    <tr>
                        <td>{kw.get('keyword', 'N/A')}</td>
                        <td>{kw.get('intent', 'N/A')}</td>
                        <td>{kw.get('competition', 'N/A')}</td>
                    </tr>
            """

        html += """
                </table>
            </div>
        </body>
        </html>
        """

        return html
