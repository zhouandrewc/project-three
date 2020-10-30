from util.modeling import prepro
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import plot_confusion_matrix

def confusion_matrix(model, X_train, X_val, y_val, weights, normalize=None, model_name=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.set(font_scale=1.5)
    sns.set_style("white")
    plot_confusion_matrix(model,prepro(X_train, X_val, scale=False)[1], y_val, sample_weight=weights[y_val.index], normalize=normalize, cmap=plt.cm.Blues,ax=ax)
    ax.set_xlabel('Predicted Status', fontsize=22, labelpad=20);
    ax.set_ylabel('True Status', fontsize=22,labelpad=20);
    ax.set_title('Confusion Matrix' + ("" if not model_name else (", " + model_name + " Model")), pad=20, fontsize=22);
    ax.xaxis.set_ticklabels(["No Bachelor's", "Bachelor's"], fontsize=20);
    ax.yaxis.set_ticklabels(["No Bachelor's", "Bachelor's"], rotation=90,fontsize=20, va="center");
    plt.show()