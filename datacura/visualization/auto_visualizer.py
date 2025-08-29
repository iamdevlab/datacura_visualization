"""
Enhanced AutoVisualizer with better bar chart handling and readability improvements.
"""
import matplotlib
matplotlib.use('Agg')
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from typing import List, Dict, Any, Optional

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

    def suggest_chart(self, column: str, dtype: str, unique_count: int) -> List[str]:
        domain_rules = {
            "generic": {
                "numeric": ["histogram", "boxplot"],
                "categorical": ["bar", "pie"] if unique_count <= 10 else ["bar"]
            },
            "education": {
                "numeric": ["histogram", "line"],
                "categorical": ["bar"] if unique_count <= 15 else ["bar"]
            },
            "supermarket": {
                "numeric": ["line", "bar"],
                "categorical": ["bar", "pie"] if unique_count <= 8 else ["bar"]
            },
            "finance": {
                "numeric": ["line", "histogram"],
                "categorical": ["bar"] if unique_count <= 12 else ["bar"]
            },
            "healthcare": {
                "numeric": ["line", "boxplot"],
                "categorical": ["bar", "pie"] if unique_count <= 7 else ["bar"]
            },
            "agriculture": {
                "numeric": ["line", "scatter"],
                "categorical": ["bar"] if unique_count <= 15 else ["bar"]
            },
            "logistics": {
                "numeric": ["line", "bar"],
                "categorical": ["bar", "pie"] if unique_count <= 6 else ["bar"]
            }
        }
        return domain_rules.get(self.domain, domain_rules["generic"]).get(dtype, ["bar"])


class AutoVisualizer:
    def __init__(self, df: pd.DataFrame, domain: str = "generic", config: Dict[str, Any] = None):
        self.df = df.copy()
        self.domain_engine = DomainRuleEngine(domain)
        default_config = {
            "max_charts_per_column": 2, 
            "export_format": "png",
            "max_categories": 20,  # Maximum categories to show in categorical charts
            "figsize_width_multiplier": 0.5,  # Width multiplier for figure size
            "dpi": 100  # Resolution for exported images
        }
        self.config = {**default_config, **(config if config else {})}

    def detect_dtype(self, column: str) -> str:
        if pd.api.types.is_numeric_dtype(self.df[column]):
            return "numeric"
        return "categorical"

    def _prepare_categorical_data(self, column: str, max_categories: Optional[int] = None):
        """Prepare categorical data, potentially limiting to top categories"""
        value_counts = self.df[column].value_counts()
        
        if max_categories and len(value_counts) > max_categories:
            # Keep top N-1 categories and group the rest as "Other"
            top_categories = value_counts.head(max_categories - 1)
            other_count = value_counts.tail(len(value_counts) - (max_categories - 1)).sum()
            
            # Create new series with top categories and "Other"
            new_series = top_categories.copy()
            new_series["Other"] = other_count
            
            return new_series, True
        return value_counts, False

    def visualize(self, export: bool = False, output_dir: str = "charts"):
        if self.df.empty:
            logger.error("DataFrame is empty. Visualization aborted.")
            return

        os.makedirs(output_dir, exist_ok=True)

        for col in self.df.columns:
            dtype = self.detect_dtype(col)
            unique_count = self.df[col].nunique()
            
            # Get chart suggestions based on domain rules and unique value count
            suggestions = self.domain_engine.suggest_chart(col, dtype, unique_count)
            suggestions = suggestions[:self.config["max_charts_per_column"]]

            for chart in suggestions:
                try:
                    # Set figure size based on expected number of categories/bars
                    if chart in ["bar", "pie"] and dtype == "categorical":
                        # For categorical charts, adjust width based on number of categories
                        num_categories = min(unique_count, self.config["max_categories"])
                        fig_width = max(8, num_categories * self.config["figsize_width_multiplier"])
                        plt.figure(figsize=(fig_width, 6))
                    else:
                        plt.figure(figsize=(10, 6))
                    
                    if chart == "histogram":
                        self.df[col].hist(bins=min(30, unique_count))
                        plt.title(f"Histogram of {col}")
                        plt.ylabel("Frequency")
                        
                    elif chart == "boxplot":
                        self.df.boxplot(column=col)
                        plt.title(f"Boxplot of {col}")
                        
                    elif chart == "bar":
                        # Handle categorical data with many values
                        data_to_plot, has_other = self._prepare_categorical_data(
                            col, self.config["max_categories"]
                        )
                        
                        ax = data_to_plot.plot(kind="bar")
                        plt.title(f"Bar chart of {col}")
                        plt.ylabel("Count")
                        
                        # Rotate labels if they're long or numerous
                        if len(data_to_plot) > 5:
                            plt.xticks(rotation=45, ha='right')
                        
                        # Add annotation if we've grouped categories
                        if has_other:
                            plt.figtext(0.02, 0.02, 
                                       f"Showing top {self.config['max_categories']-1} categories, rest grouped as 'Other'", 
                                       fontsize=8, style='italic')
                    
                    elif chart == "pie":
                        # Only create pie charts for reasonable number of categories
                        if unique_count > 15:
                            logger.warning(f"Skipping pie chart for {col}: too many categories ({unique_count})")
                            plt.close()
                            continue
                            
                        data_to_plot, has_other = self._prepare_categorical_data(
                            col, min(10, self.config["max_categories"])
                        )
                        
                        # Create pie chart
                        wedges, texts, autotexts = data_to_plot.plot(
                            kind="pie", 
                            autopct='%1.1f%%',
                            startangle=90,
                            labels=None  # We'll add legend instead for clarity
                        )
                        
                        plt.title(f"Pie chart of {col}")
                        plt.ylabel("")  # Remove y-label
                        
                        # Add legend
                        plt.legend(wedges, data_to_plot.index,
                                  title="Categories",
                                  loc="center left",
                                  bbox_to_anchor=(1, 0, 0.5, 1))
                    
                    elif chart == "line":
                        # For line charts, we need a meaningful x-axis
                        if self.df.index.dtype.kind in 'biufc':  # numeric index
                            self.df[col].plot(kind="line")
                        else:
                            # Reset index to use numeric x-axis for non-numeric indices
                            reset_df = self.df.reset_index()
                            plt.plot(reset_df.index, reset_df[col])
                        
                        plt.title(f"Line chart of {col}")
                        plt.xlabel("Index")
                    
                    elif chart == "scatter":
                        if len(self.df.columns) > 1:
                            # Find a suitable numeric column for x-axis
                            numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
                            if numeric_cols and col in numeric_cols:
                                x_col = numeric_cols[0] if numeric_cols[0] != col else numeric_cols[1] if len(numeric_cols) > 1 else self.df.columns[0]
                                self.df.plot(kind="scatter", x=x_col, y=col)
                                plt.title(f"Scatter plot of {x_col} vs {col}")
                            else:
                                logger.warning(f"Scatter plot skipped: no suitable numeric columns in {col}.")
                                plt.close()
                                continue
                        else:
                            logger.warning(f"Scatter plot skipped: not enough columns in {col}.")
                            plt.close()
                            continue

                    # Improve layout to prevent label cutoff
                    plt.tight_layout()
                    
                    if export:
                        file_path = os.path.join(output_dir, f"{col}_{chart}.{self.config['export_format']}")
                        plt.savefig(file_path, dpi=self.config["dpi"], bbox_inches='tight')
                        logger.info(f"Exported {file_path}")
                    
                    plt.close()
                    
                except Exception as e:
                    logger.error(f"Error visualizing {col} with {chart}: {e}")
                    plt.close()