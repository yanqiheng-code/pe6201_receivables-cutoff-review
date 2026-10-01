
import os
BACKEND = "preview"  # preview, baseline, live
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4.1-mini"
BASE_URL = "https://openrouter.ai/api/v1"
DATASET = "formal_test_80"  # or development_examples_20
RUN_ALL = True
CASE_ID = "TEST-001"
