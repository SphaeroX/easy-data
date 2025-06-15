from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import openai


class Visualizer:
    """Generates charts from sensor data."""

    @staticmethod
    def plot_static(
        df: pd.DataFrame,
        title: str,
        output: str,
        chart_type: str = "line",
    ) -> str:
        """Save a static chart of the DataFrame and return the file path."""

        match chart_type.lower():
            case "line":
                df.plot(figsize=(12, 5))
            case "bar":
                df.plot.bar(figsize=(12, 5))
            case "pie":
                df.iloc[-1].plot.pie(autopct="%1.1f%%")
            case _:
                raise ValueError(f"Unsupported chart type: {chart_type}")

        plt.title(title)
        if chart_type != "pie":
            plt.grid(True)
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        return output

    @staticmethod
    def plot_dynamic(
        df: pd.DataFrame,
        instructions: str,
        output: str,
        model: str = "gpt-4",
    ) -> str:
        """Use an LLM to create a custom chart and return the output path."""

        prompt = (
            "You are a Python charting assistant. "
            "Given a pandas DataFrame named df, follow the user instructions "
            "to plot the data using matplotlib. "
            "Save the figure to the path stored in the variable 'output'."
        )

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": instructions},
            ],
            temperature=0,
        )

        code = response.choices[0].message.content
        exec_env = {"df": df, "plt": plt, "output": output}
        exec(code, exec_env)
        plt.close()
        return output
