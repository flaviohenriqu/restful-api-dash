import pytest

from unittest.mock import patch

import pandas as pd


def test_ping(test_app):
    response = test_app.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


@pytest.mark.freeze_time("2023-02-19")
@pytest.mark.parametrize("data, expected", [
    (
        {"start": "2023-02-20", "end": "2023-02-20"},
        "Start date invalid",
    ),
    (
        {"start": "2023-02-18", "end": "2023-02-02"},
        "start date cannot be greater than end date",
    ),
])
def test_summary_dates_invalid(data, expected, test_app):
    response = test_app.post("/summary", params=data)
    assert response.status_code == 400
    assert expected in response.json()["message"]


@pytest.mark.freeze_time("2023-02-19")
@pytest.mark.parametrize("data, expected", [
    (
        {"start": "2023-02-18", "end": "2023-02-19"},
        {
            "('review_time', 'mean')": {'A': 14.5, 'B': 11.0, 'C': 53.5},
            "('review_time', 'median')": {'A': 18.0, 'B': 11.0, 'C': 53.5},
            "('review_time', 'mode')": {'A': 18, 'B': [1, 21], 'C': [19, 88]},
            "('review_time', 'min')": {'A': 2, 'B': 1, 'C': 19},
            "('review_time', 'max')": {'A': 20, 'B': 21, 'C': 88},
            "('merge_time', 'mean')": {'A': 1.75, 'B': 5.0, 'C': 6.5},
            "('merge_time', 'median')": {'A': 1.5, 'B': 5.0, 'C': 6.5},
            "('merge_time', 'mode')": {'A': 1, 'B': [4, 6], 'C': [6, 7]},
            "('merge_time', 'min')": {'A': 1, 'B': 4, 'C': 6},
            "('merge_time', 'max')": {'A': 3, 'B': 6, 'C': 7}
        },
    ),
])
@patch("pandas.read_sql")
def test_summary_success(mock_read_sql, data, expected, test_app):
    values = {
        "team": ["A", "B", "C", "A", "A", "B", "C", "A"],
        "review_time": [20, 21, 19, 18, 2, 1, 88, 18],
        "date": [
            "2023-02-18",
            "2023-02-18",
            "2023-02-18",
            "2023-02-19",
            "2023-02-21",
            "2023-02-19",
            "2023-02-19",
            "2023-02-17",
        ],
        "merge_time": [1, 4, 6, 1, 3, 6, 7, 2],
    }
    mock_read_sql.return_value = pd.DataFrame(values)
    response = test_app.post("/summary", params=data)
    assert response.status_code == 200
    assert response.json() == expected
