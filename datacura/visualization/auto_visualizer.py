"""
AutoVisualizer with logging, error handling, domain rules, and export support.
"""
import matplotlib
matplotlib.use('Agg')
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

from typing import List, Dict, Any

# Setup logging
logger = logging.getLogger("AutoVisualizer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class DomainRuleEngine:
    def __init__(self, domain: str = "generic"):
        self.domain = domain

    def suggest_chart(self, column: str, dtype: str) -> List[str]:
        domain_rules = {
            "generic": {
                "numeric": ["histogram", "boxplot"],
                "categorical": ["bar", "pie"]
            },
            "education": {
                "numeric": ["histogram", "line"],
                "categorical": ["bar"]
            },
            "supermarket": {
                "numeric": ["line", "bar"],
                "categorical": ["bar", "pie"]
            },
            "finance": {
                "numeric": ["line", "histogram"],
                "categorical": ["bar"]
            },
            "healthcare": {
                "numeric": ["line", "boxplot"],
                "categorical": ["bar", "pie"]
            },
            "agriculture": {
                "numeric": ["line", "scatter"],
                "categorical": ["bar"]
            },
            "logistics": {
                "numeric": ["line", "bar"],
                "categorical": ["bar", "pie"]
            }
        }
        return domain_rules.get(self.domain, domain_rules["generic"]).get(dtype, ["bar"])


class AutoVisualizer:
    def __init__(self, df: pd.DataFrame, domain: str = "generic", config: Dict[str, Any] = None):
        self.df = df
        self.domain_engine = DomainRuleEngine(domain)
        self.config = config if config else {"max_charts_per_column": 2, "export_format": "png"}

    def detect_dtype(self, column: str) -> str:
        if pd.api.types.is_numeric_dtype(self.df[column]):
            return "numeric"
        return "categorical"

    def visualize(self, export: bool = False, output_dir: str = "charts"):
        if self.df.empty:
            logger.error("DataFrame is empty. Visualization aborted.")
            return

        os.makedirs(output_dir, exist_ok=True)

        for col in self.df.columns:
            dtype = self.detect_dtype(col)
            suggestions = self.domain_engine.suggest_chart(col, dtype)[:self.config["max_charts_per_column"]]

            for chart in suggestions:
                try:
                    plt.figure()
                    if chart == "histogram":
                        self.df[col].hist()
                        plt.title(f"Histogram of {col}")
                    elif chart == "boxplot":
                        self.df.boxplot(column=col)
                        plt.title(f"Boxplot of {col}")
                    elif chart == "bar":
                        self.df[col].value_counts().plot(kind="bar")
                        plt.title(f"Bar chart of {col}")
                    elif chart == "pie":
                        self.df[col].value_counts().plot(kind="pie", autopct='%1.1f%%')
                        plt.title(f"Pie chart of {col}")
                    elif chart == "line":
                        self.df[col].plot(kind="line")
                        plt.title(f"Line chart of {col}")
                    elif chart == "scatter":
                        if len(self.df.columns) > 1:
                            self.df.plot(kind="scatter", x=self.df.columns[0], y=col)
                            plt.title(f"Scatter plot of {self.df.columns[0]} vs {col}")
                        else:
                            logger.warning(f"Scatter plot skipped: not enough columns in {col}.")
                            continue

                    if export:
                        file_path = os.path.join(output_dir, f"{col}_{chart}.{self.config['export_format']}")
                        plt.savefig(file_path)
                        logger.info(f"Exported {file_path}")
                    plt.close()
                except Exception as e:
                    logger.error(f"Error visualizing {col} with {chart}: {e}")
