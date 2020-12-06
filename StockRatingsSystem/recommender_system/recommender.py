import pandas as pd
import numpy as np


def norm(q):
    if q.shape[0] == 1:
        q = q.to_numpy()
        q = q[0]
        # square root of the sum of the squares of the components is L2 distance, Euclidean norm etc.
        return np.sqrt(q.dot(q))
    else:
        # q.shape[0] > 1:
        return (q * q).sum(axis=1)


def main(stock_symbol):
    df_new = pd.read_csv('recommender_system/reco_data.csv', index_col=1)
    pd.set_option('display.max_columns', None)
    # print(df_new[0:5])

    exclude_row = df_new.index.isin([stock_symbol])

    Q = df_new[exclude_row]
    W = df_new[~exclude_row]

    Q_L2 = norm(Q)

    W_L2 = norm(W)

    Q = Q / Q_L2

    W = pd.DataFrame.divide(W, norm(W), axis='rows')

    reco_list = W.mul(Q.to_numpy(), axis=1).sum(axis=1).nlargest(5).index.tolist()
    print('reco_list: ', reco_list)

    xrecoList = df_new.index.isin(reco_list)
    recoDF = df_new[xrecoList]
    recoDF['Symbol'] = recoDF.index

    print('recoDF: ', recoDF)

    return recoDF

if __name__ == '__main__':
    stock_symbol = "AAPL"
    main(stock_symbol)
