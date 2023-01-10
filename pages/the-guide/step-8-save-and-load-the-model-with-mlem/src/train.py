import os
import pickle
import sys

import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier

from mlem.api import load, save

params = yaml.safe_load(open("params.yaml"))["train"]

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython train.py features model\n")
    sys.exit(1)

input = sys.argv[1]
output = sys.argv[2]
seed = params["seed"]
n_est = params["n_est"]
min_split = params["min_split"]

with open(os.path.join(input, "train.pkl"), "rb") as fd:
    matrix, _ = pickle.load(fd)

labels = np.squeeze(matrix[:, 1].toarray())
x = matrix[:, 2:].toarray()

sys.stderr.write("Input matrix size {}\n".format(matrix.shape))
sys.stderr.write("X matrix size {}\n".format(x.shape))
sys.stderr.write("Y matrix size {}\n".format(labels.shape))

clf = RandomForestClassifier(
    n_estimators=n_est, min_samples_split=min_split, n_jobs=2, random_state=seed
)

clf.fit(x, labels)

tfidf = load("data/features/tfidf")
vectorizer = load("data/features/vectorizer")

save(
    clf,
    output,
    # Remove the `.toarray()` when the following PR is merged: https://github.com/iterative/mlem/pull/538
    preprocess=lambda x: tfidf(vectorizer(x)).toarray(),
    sample_data=["This is a sample text."]
)
