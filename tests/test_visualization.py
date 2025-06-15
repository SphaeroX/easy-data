import sys
import pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from easydata.visualization import Visualizer


def test_plot_static_line(tmp_path):
    df = pd.DataFrame({"a": [1, 2, 3]})
    out = tmp_path / "line.png"
    Visualizer.plot_static(df, "Title", str(out), "line")
    assert out.exists()


def test_plot_dynamic(monkeypatch, tmp_path):
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    out = tmp_path / "dyn.png"

    class FakeChoice:
        def __init__(self, content):
            self.message = type("obj", (), {"content": content})

    class FakeResponse:
        def __init__(self, content):
            self.choices = [FakeChoice(content)]

    def fake_create(**kwargs):
        code = "plt.plot(df.x, df.y); plt.savefig(output)"
        return FakeResponse(code)

    monkeypatch.setattr("openai.ChatCompletion.create", fake_create)

    Visualizer.plot_dynamic(df, "plot line", str(out))
    assert out.exists()
