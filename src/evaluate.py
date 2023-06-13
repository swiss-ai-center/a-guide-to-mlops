import json
import pickle
import sys
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

# Matplotlib config
sns.set_style("whitegrid")


def get_model_metrics(y_test: np.ndarray, predictions: np.ndarray) -> dict[str, float]:
    """Calculate the model metrics

    accuracy: the fraction of predictions our model got right
    precision: the fraction of true positives out of all positive predictions
    avg_precision: the average precision across all possible thresholds
    recall: the fraction of true positives out of all the actual positives
    f1: the harmonic mean of precision and recall
    auc: the area under the ROC curve
    """
    return {
        "accuracy": metrics.accuracy_score(y_test, predictions),
        "precision": metrics.precision_score(y_test, predictions),
        "avg_precision": metrics.average_precision_score(y_test, predictions),
        "recall": metrics.recall_score(y_test, predictions),
        "f1": metrics.f1_score(y_test, predictions),
        "auc": metrics.roc_auc_score(y_test, predictions),
    }


def plot_feature_importances(
    model: RandomForestClassifier, columns: List[str]
) -> plt.Figure:
    """Plot the feature importances of the model"""
    # Calculate feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Rearrange feature names so they match the sorted feature importances
    names = [columns[i] for i in indices]

    # Plot feature importances
    fig = plt.figure(tight_layout=True)
    plt.bar(range(len(columns)), importances[indices])
    plt.xticks(range(len(columns)), names, rotation=90)
    plt.ylabel("Importance")
    plt.title("Feature Importance")

    return fig


def plot_roc_curve(y_test: np.ndarray, predictions_proba: np.ndarray) -> plt.Figure:
    """Plot the ROC curve"""
    fpr, tpr, _ = metrics.roc_curve(y_test, predictions_proba)

    fig = plt.figure(tight_layout=True)
    plt.plot(fpr, tpr, color="darkorange", lw=2, label="ROC curve")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC curve")
    plt.legend(loc="lower right")

    return fig


def plot_confusion_matrix(y_test: np.ndarray, predictions: np.ndarray) -> plt.Figure:
    """Plot the confusion matrix"""
    matrix = metrics.confusion_matrix(y_test, predictions)
    matrix = matrix.astype("float") / matrix.sum(axis=1)[:, np.newaxis]

    fig = plt.figure(figsize=(6, 5), tight_layout=True)
    sns.heatmap(matrix, annot=True, annot_kws={"size": 14}, cmap="coolwarm")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Confusion Matrix")

    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate.py <model-path> <prepared-dataset-folder>\n")
        exit(1)

    model_path = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    evaluation_folder = Path("evaluation")
    plots_folder = Path("plots")

    # Create folders
    (evaluation_folder / plots_folder).mkdir(parents=True, exist_ok=True)

    # Load files
    labels = None
    with open(prepared_dataset_folder / "labels.json", "r") as f:
        labels = json.load(f)
        # Remove the "Habitability" label as this is what we are trying to predict
        labels = list(filter(lambda x: x != "Habitability", labels))

    X_test = np.load(prepared_dataset_folder / "X_test.npy")
    y_test = np.load(prepared_dataset_folder / "y_test.npy")

    # Load model
    model = None
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Predict on test set
    y_pred = model.predict(X_test)
    preds_by_class = model.predict_proba(X_test)
    preds = preds_by_class[:, 1]

    # Log metrics
    model_metrics = get_model_metrics(y_test, y_pred)
    for metric, value in model_metrics.items():
        print(f"{metric}: {value}")

    # Plot feature importances
    fig = plot_feature_importances(model, labels)
    fig.savefig(evaluation_folder / plots_folder / "feature_importance.png")

    # Plot ROC curve with thresholds
    fig = plot_roc_curve(y_test, preds)
    fig.savefig(evaluation_folder / plots_folder / "roc_curve.png")

    # Calculate classification report
    cr = metrics.classification_report(y_test, y_pred, output_dict=True)
    cr_df = pd.DataFrame(cr).transpose()
    cr_df.to_csv(evaluation_folder / "classification_report.csv")

    # Plot confusion matrix
    fig = plot_confusion_matrix(y_test, y_pred)
    fig.savefig(evaluation_folder / plots_folder / "confusion_matrix.png")

    print(f"Evaluation metrics and plot files saved at {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
