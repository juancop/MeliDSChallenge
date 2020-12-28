def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        import matplotlib
        matplotlib.rcParams.update({'font.size': 8})
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.metrics import confusion_matrix
        from sklearn.utils.multiclass import unique_labels
        
        cmap=plt.cm.Blues
        if not title:
            if normalize:
                title = 'Normalized confusion matrix'
            else:
                title = 'Confusion matrix, without normalization'

        cm = confusion_matrix(y_true, y_pred)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        else:
            pass


        fig, ax = plt.subplots(figsize = (6, 6))
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.figure.colorbar(im, ax=ax)
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=classes, yticklabels=classes,
               title=title,
               ylabel='Etiqueta verdadera',
               xlabel='Predicción del modelo')

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        fmt = '.0%' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]): 
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        fig.tight_layout()
        plt.show()
        return fig
