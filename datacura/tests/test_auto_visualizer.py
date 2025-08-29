import os
import pandas as pd
from datacura.visualization.auto_visualizer import AutoVisualizer, DomainRuleEngine

def test_dtype_detection():
    df = pd.DataFrame({
        "scores": [50, 60, 70],
        "grades": ["A", "B", "C"]
    })
    vis = AutoVisualizer(df)
    assert vis.detect_dtype("scores") == "numeric"
    assert vis.detect_dtype("grades") == "categorical"

def test_domain_rules():
    engine = DomainRuleEngine("education")
    assert "line" in engine.suggest_chart("scores", "numeric")

def test_visualization_export(tmp_path):
    df = pd.DataFrame({
        "scores": [50, 60, 70],
        "grades": ["A", "B", "C"]
    })
    vis = AutoVisualizer(df, domain="education", config={"max_charts_per_column": 1, "export_format": "png"})
    vis.visualize(export=True, output_dir=tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) > 0
