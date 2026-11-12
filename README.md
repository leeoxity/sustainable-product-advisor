# Sustainable Product Advisor

CPCS-331 group project — Streamlit + Python + Experta.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Publish as a website

1. Create a GitHub repository (e.g., `sustainable-product-advisor`).
2. Upload `streamlit_app.py`, `sustainable_advisor_engine.py`, `requirements.txt`, and `.streamlit/config.toml` to its root.
3. Open https://share.streamlit.io and sign in with GitHub.
4. Choose **Create app**, select your repository and branch, and use `streamlit_app.py` as the main file.
5. Press **Deploy**. Share the generated `*.streamlit.app` URL with the instructor.

The instructor needs only the link. Keep the original `.py` files and report PDF in the mandatory submission ZIP.

**Note:** The team should verify Rules 8–9, priorities, and all test cases before submitting. Experta is an older library; if a deployment error occurs, check Streamlit Cloud logs for a dependency/Python compatibility issue.
