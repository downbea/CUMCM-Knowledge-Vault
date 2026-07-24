import json
from pathlib import Path

from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_moons
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def main():
    X, y = make_moons(n_samples=220, noise=.25, random_state=2026)
    classifier = CalibratedClassifierCV(
        SVC(C=2, gamma='scale', random_state=2026),
        method='sigmoid',
        cv=5,
        ensemble=False,
    )
    model = make_pipeline(StandardScaler(), classifier)
    save({'cv_auc': cross_val_score(model, X, y, cv=5, scoring='roc_auc').mean()})


def save(o):
    p = Path(__file__).parent / 'output'
    p.mkdir(exist_ok=True)
    (p / 'result.json').write_text(json.dumps(o, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
