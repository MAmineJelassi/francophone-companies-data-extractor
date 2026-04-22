import os
import logging
from datetime import datetime
from utils.excel_handler import ExcelHandler
from automation.linkedin_navigator import LinkedInNavigator
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AutomationAgent:
    def __init__(self):
        self.config = Config()
        self.excel_handler = ExcelHandler()
        self.linkedin_nav = LinkedInNavigator(self.config)
        self.results = []

    def run(self):
        """Main automation workflow"""
        try:
            logger.info("Starting automation agent...")

            input_file = self.config.FILE_PATHS['input']
            output_file = self.config.FILE_PATHS['output']

            # Read companies from Excel
            companies = self.excel_handler.read_companies(input_file)
            logger.info(f"Loaded {len(companies)} companies from Excel")

            # Process each company
            for idx, company in enumerate(companies, 1):
                logger.info(f"Processing company {idx}/{len(companies)}: {company}")

                try:
                    # Search company on LinkedIn
                    contacts = self.linkedin_nav.search_and_extract(company)

                    # Store results
                    for contact in contacts:
                        self.results.append({
                            'Company': company,
                            'Name': contact.get('name', 'N/A'),
                            'Role': contact.get('role', 'N/A'),
                            'Email': contact.get('email', 'N/A'),
                            'Phone': contact.get('phone', 'N/A'),
                            'LinkedIn Profile': contact.get('linkedin_url', 'N/A'),
                            'Extracted At': datetime.now().isoformat()
                        })

                    logger.info(f"Extracted {len(contacts)} contacts for {company}")

                except Exception as e:
                    logger.error(f"Error processing {company}: {str(e)}")
                    continue

            # Export results to Excel
            self.excel_handler.write_results(output_file, self.results)
            logger.info(f"Results saved to {output_file}")

            logger.info("Automation completed successfully")

        except Exception as e:
            logger.error(f"Fatal error in automation: {str(e)}")
            raise
        finally:
            self.linkedin_nav.close()

if __name__ == '__main__':
    agent = AutomationAgent()
    agent.run()