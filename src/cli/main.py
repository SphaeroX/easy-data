import argparse

from easydata.config import load_influx_config
from easydata.retrieval import DataRetriever
from easydata.visualization import Visualizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query sensor data from InfluxDB and generate a chart"
    )
    parser.add_argument("query", help="Flux query to execute")
    parser.add_argument("--title", default="Sensor Data", help="Chart title")
    parser.add_argument("--output", default="output.png", help="Output image path")
    parser.add_argument(
        "--chart",
        default="line",
        choices=["line", "bar", "pie"],
        help="Type of static chart to generate",
    )
    parser.add_argument(
        "--prompt",
        help="LLM instructions for dynamic visualization; overrides --chart",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_influx_config()
    retriever = DataRetriever(config)
    df = retriever.query(args.query)

    if args.prompt:
        Visualizer.plot_dynamic(df, args.prompt, args.output)
    else:
        Visualizer.plot_static(df, args.title, args.output, args.chart)

    print(f"Chart saved to {args.output}")


if __name__ == "__main__":
    main()
