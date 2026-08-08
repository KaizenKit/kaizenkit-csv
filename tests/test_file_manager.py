import pandas as pd

from kaizenkit_csv.utils.file_manager import save_csv


def test_save_csv(tmp_path, monkeypatch):
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 25],
        }
    )

    output_path = tmp_path / "test_output.csv"

    def fake_get_save_file_name(*args, **kwargs):
        return str(output_path), "CSV Files (*.csv)"

    monkeypatch.setattr(
        "kaizenkit_csv.utils.file_manager.QFileDialog.getSaveFileName",
        fake_get_save_file_name,
    )

    saved_path = save_csv(df)

    assert saved_path == str(output_path)
    assert output_path.exists()

    loaded_df = pd.read_csv(
        output_path,
        encoding="utf-8-sig",
    )

    pd.testing.assert_frame_equal(
        df,
        loaded_df,
    )