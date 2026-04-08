# Commercial Calculators MVP (Python)

MVP project scaffold for commercial calculators to estimate sales driver payback:
- Presence uplift
- Promo ROI
- Price impact (elasticity)
- Unified scenario engine

## Stack

- Python 3.11
- pandas
- numpy
- scikit-learn
- pydantic
- streamlit
- pytest

## Project Structure

```text
.
|-- app
|   `-- streamlit_app.py
|-- calculators
|   |-- __init__.py
|   |-- presence_calculator.py
|   |-- price_impact_calculator.py
|   |-- promo_roi_calculator.py
|   `-- scenario_calculator.py
|-- models
|   |-- __init__.py
|   |-- presence_model.py
|   |-- price_model.py
|   `-- promo_model.py
|-- tests
|   `-- test_calculators.py
|-- config.py
|-- requirements.txt
`-- README.md
```

## Quick Start

1. Create and activate virtual environment.
2. Install dependencies.
3. Run tests.
4. Launch Streamlit app.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
streamlit run app/streamlit_app.py
```

## Publish to Git + Streamlit Community Cloud

1. Initialize git repository and create first commit:

```powershell
git init
git add .
git commit -m "Initial commit: streamlit calculators app"
```

2. Create an empty GitHub repository and link local project:

```powershell
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

3. Deploy in Streamlit Community Cloud:
- Open https://share.streamlit.io/
- Connect your GitHub account
- Select the repository/branch (`main`)
- Set app file path to `app/streamlit_app.py`
- Click **Deploy**

After every new change:

```powershell
git add .
git commit -m "Update app"
git push
```

## Architecture Notes

- `models/` contains typed input/output schemas (Pydantic) for validation and clear contracts.
- `calculators/` contains pure business logic with small, testable functions.
- `app/streamlit_app.py` is a thin UI layer that calls calculators and displays outputs.
- `tests/` validates baseline calculator behavior for regression safety.

This structure is intentionally lightweight, easy to extend with:
- new driver models (e.g., shelf, availability),
- data integration layer (SQL marts),
- model training pipelines (scikit-learn),
- scenario persistence and user management.
