import pickle
import sqlite3
import numpy as np
from vectorizer import vect


#更新模型方法，每次更新10000條評論
def update_pkl(db_path,clf,batch_size=10000):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * from review")
    #獲取到所有的評論
    results = c.fetchmany(batch_size)
    while results:
        data = np.array(results)
        #獲取評論
        X = data[:,1]
        #獲取
        Y = int(data[:,2])
        classes = np.array([0,1])
        #將評論轉成特徵向量
        x_train = vect.transform(X)
        #更新模型
        clf.partial_fit(x_train,Y,classes=classes)
        results = c.fetchmany(batch_size)
    conn.close()
    return None

if __name__ == "__main__":
    #加載模型
    clf = pickle.load(open("pkl/classifier.pkl", "rb"))
    #更新模型
    update_pkl("db/move_review.db",clf)
    #保存模型
    pickle.dump(clf,open("pkl/classifier.pkl","wb"),protocol=4)
