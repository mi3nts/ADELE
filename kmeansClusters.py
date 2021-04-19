import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# csv_path = "../BM3/BM3/objects/2020/06/04/T05/U00T/ADELE/2020_06_04_T05_U00T_ADELE.csv"

def createClusters(data, k):
    # data = pd.read_csv(csv)

    df = data.dropna()

    # frontal theta activity is proportional to difficulty of mental operations
    # 4-7 Hz, cognitive processing across brain regions that are further apart
    # theta = df[df.filter(like="theta").columns]

    # increased levels of alpha band power during mental and physical relaxation with eyes closed
    # so, alpha power suppressed when eyes open
    # 8-12 Hz
    # beta = df[df.filter(like="beta").columns]

    # active, busy, or anaxious thinking and active concentration correlate with higher beta power
    # 12-25 HZ
    alpha = df[df.filter(like="alpha").columns]

    model = KMeans(n_clusters=k)
    alpha_labels = model.fit_predict(alpha)
    alpha['labels'] = alpha_labels.tolist()

    class_label = [j for j in range(k)]

    class_indexes = {}

    for i in class_label:
        class_df = alpha.loc[alpha['labels'] == i]

        class_indexes[i] = [class_df.index[0], class_df.index[-1]]

    class_indexes = {a: b for a, b in sorted(class_indexes.items(), key=lambda item: item[1])}

    ordered_class = dict(zip(class_label, class_indexes.values()))

    # for i in class_indexes.items():
    #     path = "../static/Page_" + str(i[0])
    #     os.makedirs(path, exist_ok=True)
        
    #     eeg_viz(df, i[1][0], i[1][1], "../static/Page_%d/" % i[0])

    return ordered_class