import pandas as pd
import ollama
import re

class OllamaBudgetAssistant:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.messages = self.load_csv()

    def load_csv(self):
        """Load WhatsApp messages from a CSV file."""
        try:
            df = pd.read_csv(self.csv_file)
            print(f"Loaded {len(df)} messages from {self.csv_file}")
            return df['Message'].tolist()  # Ensure 'Message' is a column in your CSV
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []

    def categorize_expenses(self):
        """Use Ollama to categorize expenses from messages."""
        categorized_data = []

        for message in self.messages:
            prompt = (
                f"Classify this message into one of the following categories: Food, Entertainment, Grocery, Miscellaneous.\n"
                f"Also, extract any expense amount if mentioned.\n\n"
                f"Message: \"{message}\"\n"
                f"Response:"
            )

            response = ollama.chat(model='deepseek-r1:8b', messages=[{'role': 'user', 'content': prompt}])
            categorized_data.append((message, response['message']['content']))

        return categorized_data

    def summarize_expenses(self, categorized_data):
        """Summarize categorized expenses into total amounts."""
        categories = {'Food': 0, 'Entertainment': 0, 'Grocery': 0, 'Miscellaneous': 0}

        for _, response in categorized_data:
            for category in categories.keys():
                if category.lower() in response.lower():
                    amount = self.extract_amount(response)
                    categories[category] += amount

        return categories

    @staticmethod
    def extract_amount(text):
        """Extract numerical expense amounts from text."""
        amounts = re.findall(r'\$\s?(\d+)', text)
        return sum(map(int, amounts)) if amounts else 0

    def get_budget_summary(self):
        """Run the full process and return the expense summary."""
        categorized_data = self.categorize_expenses()
        summary = self.summarize_expenses(categorized_data)
        return summary
