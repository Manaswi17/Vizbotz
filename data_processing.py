import pandas as pd
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import streamlit as st

class Process_data:

    def __init__(self, data):
        self.data = pd.read_csv(data)
        load_dotenv()
        self.gemini_api_key = st.secrets("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def get_df(self):
        return self.data

    def get_columns(self):
        return self.data.columns.to_list()

    def get_mean(self, col_name):
        return self.data[col_name].mean()

    def describe_data(self):
        return self.data.describe()

    def generate_chart_summary(self, x_column, y_column=None, top_n=5):
        summary = {}
        if y_column and self.data[y_column].dtype in ["int64", "float64"]:
            top_samples = self.data[[x_column, y_column]].sort_values(by=y_column, ascending=False).head(top_n)
            bottom_samples = self.data[[x_column, y_column]].sort_values(by=y_column, ascending=True).head(top_n)
            summary["top_samples"] = top_samples.to_dict(orient="records")
            summary["bottom_samples"] = bottom_samples.to_dict(orient="records")
            stats = self.data[y_column].describe().to_dict()
            summary["stats"] = {
                "mean": stats.get("mean"),
                "std_dev": stats.get("std"),
                "min": stats.get("min"),
                "max": stats.get("max"),
                "count": stats.get("count")
            }
        else:
            counts = self.data[x_column].value_counts().reset_index()
            counts.columns = [x_column, "count"]
            summary["top_samples"] = counts.head(top_n).to_dict(orient="records")
            summary["bottom_samples"] = counts.tail(top_n).to_dict(orient="records")
            summary["stats"] = {"total_categories": len(counts)}
        return summary

    def generate_insights_from_vega(self, vega_spec, x_column, y_column=None):
        try:
            summary = self.generate_chart_summary(x_column, y_column)
            prompt = f"""
You are a senior data analyst reviewing a dataset visualization.

Chart Type: {vega_spec.get('mark', 'Unknown')}
X-axis: {x_column}
Y-axis: {y_column if y_column else 'N/A'}

Top Samples:
{json.dumps(summary.get("top_samples", []), indent=2)}

Bottom Samples:
{json.dumps(summary.get("bottom_samples", []), indent=2)}

Stats:
{json.dumps(summary.get("stats", {}), indent=2)}

Return response strictly in this JSON format:
{{
  "key_observations": [...],
  "trends_or_patterns": "...",
  "anomalies_or_outliers": "...",
  "recommendations": [...],
  "summary": [...]
}}
            """
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1024,
                )
            )
            return self._parse_gemini_response(response)

        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return {"error": str(e), "raw_response": "Failed to generate insight."}

    def _parse_gemini_response(self, response):
        try:
            content = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
            match = re.search(r'\{[\s\S]*?\}', content)
            if match:
                return json.loads(match.group(0))
            return {
                "key_observations": [],
                "trends_or_patterns": "",
                "anomalies_or_outliers": "",
                "recommendations": [],
                "summary": ["Could not parse structured JSON."]
            }
        except Exception as e:
            return {
                "error": str(e),
                "summary": ["Parser failed."],
                "raw_response": str(response)
            }

    def generate_vegalite_spec(self, chart_type, x_column, y_column=None, color_column=None, insights=None):
        chart_data = self.data.copy()
        if len(chart_data) > 10000:
            chart_data = chart_data.sample(10000)

        base_spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": f"{chart_type.capitalize()} chart of {x_column}" + (f" vs {y_column}" if y_column else ""),
            "data": {"values": chart_data.to_dict(orient="records")},
            "width": 650,
            "height": 400
        }

        encoding = {}

        if chart_type == "line":
            base_spec["mark"] = {"type": "line", "interpolate": "monotone"}
            encoding["x"] = {"field": x_column, "type": "quantitative", "sort": True}
            encoding["y"] = {"field": y_column, "type": "quantitative"}
            if color_column:
                encoding["color"] = {"field": color_column, "type": "nominal"}

        elif chart_type in ["scatter", "point"]:
            base_spec["mark"] = "point"
            encoding["x"] = {"field": x_column, "type": "quantitative"}
            encoding["y"] = {"field": y_column, "type": "quantitative"}
            if color_column:
                encoding["color"] = {"field": color_column, "type": "nominal"}

        elif chart_type == "bar":
            base_spec["mark"] = "bar"
            encoding["x"] = {"field": x_column, "type": "nominal"}
            encoding["y"] = {"field": y_column, "type": "quantitative"}
            if color_column:
                encoding["color"] = {"field": color_column, "type": "nominal"}

        elif chart_type == "boxplot":
            base_spec["mark"] = "boxplot"
            encoding["x"] = {"field": x_column, "type": "nominal"}
            encoding["y"] = {"field": y_column, "type": "quantitative"}

        elif chart_type == "arc":
            base_spec["mark"] = {"type": "arc", "innerRadius": 0}
            encoding = {
                "theta": {"field": x_column, "aggregate": "count", "type": "quantitative"},
                "color": {"field": x_column, "type": "nominal"}
            }

        else:
            base_spec["mark"] = chart_type
            encoding["x"] = {"field": x_column, "type": "quantitative"}
            if y_column:
                encoding["y"] = {"field": y_column, "type": "quantitative"}

        base_spec["encoding"] = encoding

        if insights and isinstance(insights, dict) and "key_observations" in insights:
            bullets = [
                {
                    "data": {"values": [{}]},
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "baseline": "top",
                        "dx": 10,
                        "dy": 10 + 20 * i,
                        "fontSize": 12
                    },
                    "encoding": {
                        "text": {"value": f"• {obs[:100]}"}
                    }
                } for i, obs in enumerate(insights["key_observations"][:3])
            ]
            return {
                "$schema": base_spec["$schema"],
                "description": base_spec["description"],
                "layer": [base_spec] + bullets
            }

        return base_spec
