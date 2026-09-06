# Калькулятор потенциала роста продаж

Streamlit-приложение для оценки, какой прирост продаж дают три рычага: представленность (presence uplift), промо (ROI) и цена (эластичность). Рычаги считаются по отдельности и собираются в один сценарий.

Стек: Python 3.11, pandas, numpy, pydantic, streamlit, pytest.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
streamlit run app/streamlit_app.py
```

## Структура

```text
app/streamlit_app.py     UI
calculators/             расчёт presence / promo ROI / price / scenario
models/                  Pydantic-схемы входов и выходов
tests/                   регрессия калькуляторов
```

`models/` задаёт контракт данных. `calculators/` — чистые функции без UI. `app/streamlit_app.py` только вызывает калькуляторы и показывает результат.
