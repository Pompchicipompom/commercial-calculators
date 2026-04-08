"""Single sales growth potential calculator UI."""

from dataclasses import dataclass
from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import settings


TITLE = "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u0430 \u0440\u043e\u0441\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0436"
CAPTION = (
    "\u0415\u0434\u0438\u043d\u044b\u0439 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0447\u0435\u0441\u043a\u0438\u0439 "
    "\u043a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0434\u043b\u044f \u043e\u0446\u0435\u043d\u043a\u0438 "
    "\u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u0430 \u0440\u043e\u0441\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0436"
)
DEVELOPER_NOTE = (
    "\u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a: "
    "\u0421\u0442\u0430\u0440\u043a\u043e\u0432 \u041e.\u0410. "
    "\u0441\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u043e \u0434\u043b\u044f "
    "\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438 \u041e\u041e\u041e "
    "\"\u041f\u0438\u0432\u043e\u0432\u0430\u0440\u0435\u043d\u043d\u0430\u044f "
    "\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \"\u0411\u0430\u043b\u0442\u0438\u043a\u0430\""
)

REGIONS = (
    "\u0426\u0435\u043d\u0442\u0440",
    "\u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434",
    "\u042e\u0433",
    "\u041f\u043e\u0432\u043e\u043b\u0436\u044c\u0435",
    "\u0421\u0438\u0431\u0438\u0440\u044c",
)
FORMATS = (
    "\u0413\u0438\u043f\u0435\u0440\u043c\u0430\u0440\u043a\u0435\u0442",
    "\u0421\u0443\u043f\u0435\u0440\u043c\u0430\u0440\u043a\u0435\u0442",
    "\u041c\u0430\u0433\u0430\u0437\u0438\u043d \u0443 \u0434\u043e\u043c\u0430",
    "\u0414\u0438\u0441\u043a\u0430\u0443\u043d\u0442\u0435\u0440",
)
PERIODS = (
    "\u041c\u0435\u0441\u044f\u0446",
    "\u041a\u0432\u0430\u0440\u0442\u0430\u043b",
    "\u041f\u043e\u043b\u0443\u0433\u043e\u0434\u0438\u0435",
)
PROMO_LEVELS = (
    "\u041d\u0435\u0442",
    "\u041d\u0438\u0437\u043a\u0430\u044f",
    "\u0421\u0440\u0435\u0434\u043d\u044f\u044f",
    "\u0412\u044b\u0441\u043e\u043a\u0430\u044f",
)

PERIOD_MULTIPLIER = {
    PERIODS[0]: 1.0,
    PERIODS[1]: 3.0,
    PERIODS[2]: 6.0,
}

PROMO_MULTIPLIER = {
    PROMO_LEVELS[0]: 1.00,
    PROMO_LEVELS[1]: 1.03,
    PROMO_LEVELS[2]: 1.07,
    PROMO_LEVELS[3]: 1.11,
}

REGION_FACTOR = {
    REGIONS[0]: 1.25,
    REGIONS[1]: 1.05,
    REGIONS[2]: 0.95,
    REGIONS[3]: 1.00,
    REGIONS[4]: 0.90,
}

FORMAT_FACTOR = {
    FORMATS[0]: 1.35,
    FORMATS[1]: 1.10,
    FORMATS[2]: 0.85,
    FORMATS[3]: 0.92,
}

TOP_STORES_BY_REGION = {
    REGIONS[0]: (
        "\u041c\u043e\u0441\u043a\u0432\u0430 \u0422\u0432\u0435\u0440\u0441\u043a\u0430\u044f",
        "\u041f\u043e\u0434\u043e\u043b\u044c\u0441\u043a \u0426\u0435\u043d\u0442\u0440",
        "\u041a\u0430\u043b\u0443\u0433\u0430 \u0421\u0435\u0432\u0435\u0440",
    ),
    REGIONS[1]: (
        "\u0421\u0430\u043d\u043a\u0442-\u041f\u0435\u0442\u0435\u0440\u0431\u0443\u0440\u0433 \u041d\u0435\u0432\u0441\u043a\u0438\u0439",
        "\u041c\u0443\u0440\u0438\u043d\u043e \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439",
        "\u041f\u0441\u043a\u043e\u0432 \u042e\u0436\u043d\u044b\u0439",
    ),
    REGIONS[2]: (
        "\u041a\u0440\u0430\u0441\u043d\u043e\u0434\u0430\u0440 \u0417\u0430\u043f\u0430\u0434",
        "\u0420\u043e\u0441\u0442\u043e\u0432 \u0421\u0435\u0432\u0435\u0440",
        "\u0421\u043e\u0447\u0438 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439",
    ),
    REGIONS[3]: (
        "\u041a\u0430\u0437\u0430\u043d\u044c \u0426\u0435\u043d\u0442\u0440",
        "\u0421\u0430\u043c\u0430\u0440\u0430 \u0412\u043e\u043b\u0433\u0430",
        "\u041d\u0438\u0436\u043d\u0438\u0439 \u041d\u043e\u0432\u0433\u043e\u0440\u043e\u0434 \u0412\u043e\u0441\u0442\u043e\u043a",
    ),
    REGIONS[4]: (
        "\u041d\u043e\u0432\u043e\u0441\u0438\u0431\u0438\u0440\u0441\u043a \u041b\u0435\u0432\u044b\u0439 \u0411\u0435\u0440\u0435\u0433",
        "\u041e\u043c\u0441\u043a \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439",
        "\u041a\u0440\u0430\u0441\u043d\u043e\u044f\u0440\u0441\u043a \u0421\u0435\u0432\u0435\u0440",
    ),
}


@dataclass(frozen=True)
class SegmentProfile:
    baseline_units_month: float
    margin_per_unit_rub: float
    focus_stores: int
    top_stores: tuple[str, str, str]


def apply_dashboard_style() -> None:
    st.markdown(
        """
        <style>
            :root {
                --surface: #ffffff;
                --surface-soft: #f6f7f9;
                --border: #dfe3ea;
                --text: #141821;
                --muted: #5e6678;
                --ok: #0c7f43;
                --warn: #c67700;
                --low: #8f2f2f;
            }

            .stApp { background: var(--surface); color: var(--text); }
            .block-container { max-width: 1180px; padding-top: 1.7rem; padding-bottom: 1.7rem; }
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stHeader"] {
                background: #ffffff !important;
                border-bottom: 1px solid var(--border) !important;
            }
            [data-testid="stDecoration"] {
                background: #ffffff !important;
            }

            /* Dark text on all white surfaces */
            .stApp, .stApp p, .stApp label, .stApp span, .stApp div, .stApp li, .stApp h1, .stApp h2, .stApp h3 {
                color: #111111 !important;
                -webkit-text-fill-color: #111111 !important;
            }

            [data-testid="stMetric"] {
                background: var(--surface-soft);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 1rem;
            }

            [data-testid="stNumberInput"] input,
            [data-testid="stSelectbox"] div[data-baseweb="select"] * {
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
            }

            [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                background: #ffffff !important;
                border: 1px solid var(--border) !important;
                border-radius: 10px;
            }

            div[data-baseweb="popover"] [role="listbox"] {
                background: #ffffff !important;
                border: 1px solid var(--border) !important;
                border-radius: 10px !important;
            }

            div[data-baseweb="popover"] [role="option"],
            div[data-baseweb="popover"] [role="option"] * {
                color: var(--text) !important;
                -webkit-text-fill-color: var(--text) !important;
                background: #ffffff !important;
            }

            div.stButton > button {
                border-radius: 10px;
                border: 1px solid #c8ced8;
                background: #ffffff;
                color: #111111;
                font-weight: 600;
                padding: 0.55rem 1rem;
            }

            div.stButton > button * {
                color: #111111 !important;
                -webkit-text-fill-color: #111111 !important;
            }

            /* Small '?' button with visible contrast */
            button[data-testid="stPopoverButton"] {
                background: #111111 !important;
                color: #ffffff !important;
                border: 1px solid #8f98a8 !important;
                border-radius: 999px !important;
                width: 1.9rem !important;
                height: 1.9rem !important;
                min-height: 1.9rem !important;
                padding: 0 !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
            }

            button[data-testid="stPopoverButton"] * {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
            }

            button[data-testid="stPopoverButton"]:hover {
                background: #1f2430 !important;
            }

            div[data-testid="stPopover"],
            div[data-testid="stTooltipContent"],
            [role="tooltip"] {
                background: #1f2430 !important;
                border: 1px solid #1f2430 !important;
                border-radius: 12px !important;
            }

            div[data-testid="stPopover"] *,
            div[data-testid="stTooltipContent"] *,
            [role="tooltip"] * {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
            }

            .note-box {
                border: 1px solid var(--border);
                border-radius: 14px;
                background: var(--surface-soft);
                padding: 0.95rem 1rem;
                color: var(--text);
            }

            .hint-text {
                color: var(--muted);
                font-size: 0.94rem;
                line-height: 1.35;
            }

            .priority-high, .priority-medium, .priority-low {
                font-weight: 700;
                border-radius: 999px;
                padding: 0.2rem 0.7rem;
                display: inline-block;
            }

            .priority-high { color: var(--ok); background: #e8f7ef; }
            .priority-medium { color: var(--warn); background: #fff4df; }
            .priority-low { color: var(--low); background: #fdecec; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def build_segment_profile(region: str, store_format: str) -> SegmentProfile:
    region_factor = REGION_FACTOR[region]
    format_factor = FORMAT_FACTOR[store_format]
    baseline_units = 8200 * region_factor * format_factor
    margin_per_unit = 34 * (0.95 + (format_factor - 0.85) * 0.6)
    focus_stores = int(140 * region_factor * format_factor)
    top_base = TOP_STORES_BY_REGION[region]
    top_stores = (
        f"{top_base[0]} ({store_format})",
        f"{top_base[1]} ({store_format})",
        f"{top_base[2]} ({store_format})",
    )
    return SegmentProfile(baseline_units, margin_per_unit, focus_stores, top_stores)


def format_number(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def calculate_growth_potential(
    profile: SegmentProfile,
    period: str,
    current_presence_pct: float,
    target_presence_pct: float,
    shelf_change_pct: float,
    promo_level: str,
) -> dict[str, float | int | str | list[tuple[str, float]]]:
    period_multiplier = PERIOD_MULTIPLIER[period]
    baseline_units_period = profile.baseline_units_month * period_multiplier
    presence_gap_pp = max(target_presence_pct - current_presence_pct, 0.0)

    base_uplift_pct = presence_gap_pp * 0.012
    shelf_multiplier = max(0.85, 1 + (shelf_change_pct / 100) * 0.35)
    promo_multiplier = PROMO_MULTIPLIER[promo_level]

    potential_growth_pct = min(base_uplift_pct * shelf_multiplier * promo_multiplier, 0.55)
    incremental_units = baseline_units_period * potential_growth_pct
    margin_effect = incremental_units * profile.margin_per_unit_rub

    if potential_growth_pct >= 0.12:
        priority = "\u0412\u044b\u0441\u043e\u043a\u0438\u0439"
        priority_class = "priority-high"
    elif potential_growth_pct >= 0.05:
        priority = "\u0421\u0440\u0435\u0434\u043d\u0438\u0439"
        priority_class = "priority-medium"
    else:
        priority = "\u041d\u0438\u0437\u043a\u0438\u0439"
        priority_class = "priority-low"

    stores_in_focus = int(profile.focus_stores * (1 + presence_gap_pp / 120))
    top_shares = (0.24, 0.17, 0.12)
    top_store_effects = [
        (name, incremental_units * share)
        for name, share in zip(profile.top_stores, top_shares, strict=False)
    ]

    return {
        "incremental_units": incremental_units,
        "potential_growth_pct": potential_growth_pct * 100,
        "margin_effect": margin_effect,
        "priority": priority,
        "priority_class": priority_class,
        "stores_in_focus": stores_in_focus,
        "top_store_effects": top_store_effects,
    }


def render_help_popover() -> None:
    with st.popover("?", help="\u0427\u0442\u043e \u044d\u0442\u043e \u0438 \u043a\u0430\u043a \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f"):
        st.markdown(
            (
                "**\u0427\u0442\u043e \u044d\u0442\u043e**\n\n"
                "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u0435\u0442 "
                "\u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b \u0440\u043e\u0441\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0436 "
                "\u0447\u0435\u0440\u0435\u0437 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c.\n\n"
                "**\u0412\u0430\u0436\u043d\u043e \u0440\u0430\u0437\u043b\u0438\u0447\u0430\u0442\u044c**\n\n"
                "- **\u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c**: "
                "\u0432 \u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u0442\u043e\u0447\u043a\u0430\u0445 \u043f\u0440\u043e\u0434\u0430\u0436 "
                "\u0442\u043e\u0432\u0430\u0440 \u0435\u0441\u0442\u044c \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438.\n"
                "- **\u041f\u043e\u043b\u043a\u0430**: \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e "
                "\u0432\u044b\u043a\u043b\u0430\u0434\u043a\u0438 \u0432\u043d\u0443\u0442\u0440\u0438 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430.\n\n"
                "1. \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0435\u0433\u0438\u043e\u043d, \u0444\u043e\u0440\u043c\u0430\u0442 "
                "\u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430 \u0438 \u043f\u0435\u0440\u0438\u043e\u0434.\n"
                "2. \u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u0438 \u0446\u0435\u043b\u0435\u0432\u043e\u0439 "
                "\u0443\u0440\u043e\u0432\u0435\u043d\u044c \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u0438.\n"
                "3. \u041d\u0430\u0436\u043c\u0438\u0442\u0435 "
                "\u00ab\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0442\u044c \u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u00bb."
            )
        )


def render_intro() -> None:
    st.markdown(
        (
            '<div class="note-box">'
            "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 "
            "\u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442, \u043a\u0430\u043a\u043e\u0439 "
            "\u043f\u0440\u0438\u0440\u043e\u0441\u0442 \u043f\u0440\u043e\u0434\u0430\u0436 "
            "\u043c\u043e\u0436\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c "
            "\u0437\u0430 \u0441\u0447\u0435\u0442 \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f "
            "\u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u0438 "
            "\u0432 \u043f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442\u043d\u044b\u0445 "
            "\u0442\u043e\u0447\u043a\u0430\u0445 \u043f\u0440\u043e\u0434\u0430\u0436."
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<p class="hint-text">'
            "\u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c "
            "\u2014 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u0434\u0440\u0430\u0439\u0432\u0435\u0440 "
            "\u0440\u0430\u0441\u0447\u0435\u0442\u0430. \u041f\u043e\u043b\u043a\u0430 \u0438 \u043f\u0440\u043e\u043c\u043e "
            "\u2014 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0444\u0430\u043a\u0442\u043e\u0440\u044b."
            "</p>"
        ),
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title=TITLE, layout="wide")
    apply_dashboard_style()

    title_col, help_col = st.columns([20, 1])
    with title_col:
        st.title(TITLE)
        st.caption(DEVELOPER_NOTE)
        st.caption(CAPTION)
    with help_col:
        st.write("")
        render_help_popover()

    render_intro()

    left_col, right_col = st.columns([1.12, 1], gap="large")

    with left_col:
        st.subheader("\u0412\u0445\u043e\u0434\u043d\u044b\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b")
        st.markdown(
            "**\u0413\u043b\u0430\u0432\u043d\u044b\u0439 \u0434\u0440\u0430\u0439\u0432\u0435\u0440: "
            "\u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c "
            "\u0432 \u0442\u043e\u0447\u043a\u0430\u0445 \u043f\u0440\u043e\u0434\u0430\u0436**"
        )
        current_presence_pct = st.slider(
            "\u0422\u0435\u043a\u0443\u0449\u0430\u044f \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c, %",
            min_value=0.0,
            max_value=100.0,
            value=64.0,
            step=1.0,
        )
        target_presence_pct = st.slider(
            "\u0426\u0435\u043b\u0435\u0432\u0430\u044f \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c, %",
            min_value=0.0,
            max_value=100.0,
            value=78.0,
            step=1.0,
        )
        st.markdown(
            "**\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 "
            "\u0444\u0430\u043a\u0442\u043e\u0440\u044b (\u043e\u043f\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e)**"
        )
        shelf_change_pct = st.slider(
            "\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 "
            "\u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e\u0441\u0442\u0438 \u043f\u043e\u043b\u043a\u0438, %",
            min_value=-10.0,
            max_value=30.0,
            value=0.0,
            step=1.0,
        )
        promo_level = st.radio(
            "\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430 \u043f\u0440\u043e\u043c\u043e",
            options=PROMO_LEVELS,
            horizontal=True,
        )
        st.markdown("**\u0424\u0438\u043b\u044c\u0442\u0440\u044b**")
        region = st.selectbox("\u0420\u0435\u0433\u0438\u043e\u043d", options=REGIONS)
        store_format = st.selectbox("\u0424\u043e\u0440\u043c\u0430\u0442 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430", options=FORMATS)
        period = st.selectbox("\u041f\u0435\u0440\u0438\u043e\u0434", options=PERIODS)

        calculate_clicked = st.button(
            "\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0442\u044c \u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b",
            use_container_width=True,
        )

        if calculate_clicked and target_presence_pct < current_presence_pct:
            st.warning(
                "\u0426\u0435\u043b\u0435\u0432\u0430\u044f \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u044c "
                "\u043d\u0438\u0436\u0435 \u0442\u0435\u043a\u0443\u0449\u0435\u0439. \u041f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b "
                "\u0440\u043e\u0441\u0442\u0430 \u0431\u0443\u0434\u0435\u0442 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d \u043a\u0430\u043a 0."
            )

        if calculate_clicked:
            profile = build_segment_profile(region, store_format)
            st.session_state["last_result"] = calculate_growth_potential(
                profile=profile,
                period=period,
                current_presence_pct=current_presence_pct,
                target_presence_pct=target_presence_pct,
                shelf_change_pct=shelf_change_pct,
                promo_level=promo_level,
            )

    with right_col:
        st.subheader("\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b")
        result = st.session_state.get("last_result")
        if result is None:
            st.info(
                "\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b "
                "\u0441\u043b\u0435\u0432\u0430 \u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 "
                "\u00ab\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0442\u044c \u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u00bb."
            )
        else:
            metric_col_1, metric_col_2 = st.columns(2)
            with metric_col_1:
                st.metric(
                    "\u041f\u0440\u043e\u0433\u043d\u043e\u0437\u043d\u044b\u0439 "
                    "\u043f\u0440\u0438\u0440\u043e\u0441\u0442 \u043f\u0440\u043e\u0434\u0430\u0436, \u0435\u0434.",
                    format_number(float(result["incremental_units"])),
                )
                st.metric(
                    "\u041e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0439 "
                    "\u043c\u0430\u0440\u0436\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0444\u0444\u0435\u043a\u0442, \u0440\u0443\u0431.",
                    format_number(float(result["margin_effect"])),
                )
            with metric_col_2:
                st.metric(
                    "\u041f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b \u0440\u043e\u0441\u0442\u0430, %",
                    f"{float(result['potential_growth_pct']):.1f}%",
                )
                st.metric(
                    "\u0422\u043e\u0447\u0435\u043a \u0432 \u0444\u043e\u043a\u0443\u0441\u0435",
                    format_number(float(result["stores_in_focus"])),
                )

            st.markdown(
                f"""
                <p>\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f:
                <span class="{result["priority_class"]}">{result["priority"]}</span>
                </p>
                """,
                unsafe_allow_html=True,
            )

            with st.expander(
                "\u0413\u0434\u0435 \u0431\u0440\u0430\u0442\u044c \u0440\u043e\u0441\u0442 \u0432 "
                "\u043f\u0435\u0440\u0432\u0443\u044e \u043e\u0447\u0435\u0440\u0435\u0434\u044c",
                expanded=True,
            ):
                st.markdown(
                    "**\u0422\u043e\u043f-3 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430 "
                    "\u0441 \u043d\u0430\u0438\u0431\u043e\u043b\u044c\u0448\u0438\u043c \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u043c**"
                )
                for name, units in result["top_store_effects"]:
                    st.write(f"- {name}: +{format_number(units)} \u0435\u0434.")

    st.markdown("---")
    st.caption(
        "\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u044d\u0444\u0444\u0435\u043a\u0442 "
        "\u0440\u0430\u0441\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u0435\u0442\u0441\u044f "
        "\u0447\u0435\u0440\u0435\u0437 \u0440\u043e\u0441\u0442 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u043e\u0441\u0442\u0438. "
        "\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u043f\u043e\u043b\u043a\u0438 \u0438 \u043f\u0440\u043e\u043c\u043e "
        "\u0443\u0447\u0438\u0442\u044b\u0432\u0430\u044e\u0442\u0441\u044f \u043a\u0430\u043a "
        "\u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0444\u0430\u043a\u0442\u043e\u0440\u044b."
    )


if __name__ == "__main__":
    main()
