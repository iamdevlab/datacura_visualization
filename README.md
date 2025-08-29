
# Datacura Visualization  

**Datacura Visualization** is a lightweight, production-ready Python library for **automatic data visualization**.  
It intelligently detects column types in datasets (numeric, categorical, datetime, text) and generates the most suitable charts automatically — with support for domain-specific data such as **education, retail, finance, healthcare, agriculture, and logistics**.  

Designed for **clarity, speed, and usability**, Datacura Visualization powers the visualization layer of the [Datacura app](https://github.com/iamdevlab/datacura), but can also be used as a standalone library.  

---

## ✨ Features  

- 🔍 **Automatic Column Detection** – figures out numeric, categorical, datetime, and text columns.  
- 📊 **Smart Chart Selection** – chooses the right visualization (bar, line, scatter, histogram, pie, etc.).  
- 🏥 **Domain-Specific Rules** – pre-configured for multiple domains:  
  - **Education** (grades, subjects, performance trends)  
  - **Retail/Supermarket** (sales, prices, categories)  
  - **Finance** (transactions, amounts, time series)  
  - **Healthcare** (patients, visits, vitals)  
  - **Agriculture** (crops, yields, seasons)  
  - **Logistics** (shipments, locations, durations)  
- 🛡️ **Robust Error Handling** – catches and logs issues without breaking.  
- 📤 **Export Ready** – save charts as PNG, JPG, or PDF.  
- 🧪 **Unit Tested** – reliable results with pytest-based tests.  

---

## 📦 Installation  

You can install directly from source:  

```bash
git clone https://github.com/iamdevlab/datacura_visualization.git
cd datacura_visualization
pip install -e .
```

---

## 🚀 Quick Start  

```python
import pandas as pd
from datacura.visualization.auto_visualizer import AutoVisualizer

# Example dataset
data = {
    "Student": ["Alice", "Bob", "Charlie", "Diana"],
    "Math": [85, 90, 78, 92],
    "English": [88, 76, 95, 89],
    "Grade": ["A", "B", "B", "A"]
}
df = pd.DataFrame(data)

# Initialize the visualizer
viz = AutoVisualizer(domain="education")

# Generate automatic charts
viz.visualize(df)

# Export charts to PNG
viz.export_charts(df, output_dir="charts", formats=["png"])
```

---

## ⚙️ Configuration  

You can customize the behavior using options:  

```python
viz = AutoVisualizer(
    domain="retail",
    save_on_error=True,        # saves empty charts if errors occur
    default_export_formats=["png", "pdf"],  # default export formats
    log_level="DEBUG"          # DEBUG / INFO / WARNING / ERROR
)
```

---

## 📤 Exporting Charts  

Charts can be exported in multiple formats:  

```python
viz.export_charts(df, output_dir="charts", formats=["png", "pdf"])
```

This will generate files like:  

```
charts/
  Math_histogram.png
  English_histogram.png
  Grade_bar.png
```

---

## 🧪 Running Tests  

The package includes unit tests. To run them:  

```bash
pytest datacura/tests/
```

---

## 📚 Domains Supported  

- **Education** – grades, scores, subjects  
- **Retail/Supermarket** – sales, categories, prices  
- **Finance** – transactions, time series, balances  
- **Healthcare** – patients, visits, vitals  
- **Agriculture** – crops, yields, seasons  
- **Logistics** – shipments, durations, locations  

---

## 🔮 Roadmap  

- Interactive charts (Plotly/Altair integration)  
- More domain-specific visualizations  
- Auto-report generation (PDF/HTML dashboards)  
- Datacura App cloud integration  

---

## 🤝 Contributing  

Pull requests are welcome! If you’d like to add new domains, improve detection logic, or extend chart types, please fork the repo and open a PR.  

---

## 📄 License  

This project is licensed under the MIT License.  


## 📊 Example Visualizations

Here are some example charts generated using **Datacura Visualization**:

### 1. School Student Performance (Scatter Plot)
![School Performance](school_performance.png)

### 2. Supermarket Sales Distribution (Bar Chart)
![Supermarket Sales](supermarket_sales.png)

### 3. Monthly Healthcare Visits (Line Chart)
![Healthcare Visits](healthcare_visits.png)

### 4. Agriculture Crop Yield (Pie Chart)
![Agriculture Yield](agriculture_yield.png)
