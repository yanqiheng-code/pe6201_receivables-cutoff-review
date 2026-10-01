"""Re-score submitted predictions offline; preserve original artifacts and make no API calls."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'local_tester'))
import run


def main():
    folders = sorted((ROOT / 'evaluation_evidence').glob('*_*'))
    checked = 0
    for folder in folders:
        if not folder.is_dir():
            continue
        manifest = json.loads((folder / 'manifest.json').read_text())
        data = json.loads((ROOT / manifest.get('dataset', 'development_examples_20') / 'inputs.json').read_text())
        assert hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest() == manifest['inputs_sha256'], 'Input version mismatch'
        prompt = (folder / 'prompt_snapshot.md').read_text(encoding='utf-8')
        assert hashlib.sha256(prompt.encode()).hexdigest() == manifest['prompt_sha256'], 'Prompt snapshot mismatch'
        records = json.loads((folder / 'results.json').read_text())
        answers = json.loads((ROOT / manifest.get('dataset', 'development_examples_20') / 'answer_key.json').read_text())['answers']
        measured = run.evaluate(records, answers, manifest['selected_ids'])
        saved = json.loads((folder / 'evaluation.json').read_text())
        for key in ('selected_cases', 'valid_predictions', 'exact_label_correct', 'amount_correct',
                    'errors_flagged', 'false_flags_on_normal_cases', 'missing_evidence_cases_correct'):
            assert measured[key] == saved[key], f'{folder.name}: mismatch in {key}'
        print(f"{folder.name}: labels {measured['exact_label_correct']}/{measured['selected_cases']}, "
              f"amounts {measured['amount_correct']}/{measured['selected_cases']} — verified")
        checked += 1
    assert checked == 5, 'Expected five preserved evaluation runs'
    print('All five submitted runs reproduce their reported counts. No API calls made.')


if __name__ == '__main__':
    main()
