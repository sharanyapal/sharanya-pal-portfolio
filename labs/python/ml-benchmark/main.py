"""Reproducible classification benchmark on the public Iris toy dataset."""
import argparse
import json
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def benchmark(seed=42):
    dataset=load_iris()
    X_train,X_test,y_train,y_test=train_test_split(dataset.data,dataset.target,test_size=.25,random_state=seed,stratify=dataset.target)
    methods={
        'Logistic Regression':Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=2000,random_state=seed))]),
        'Random Forest':RandomForestClassifier(n_estimators=100,random_state=seed),
        'SVM (RBF)':Pipeline([('scale',StandardScaler()),('model',SVC(kernel='rbf',random_state=seed))]),
    }
    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=seed)
    results={}
    for name,model in methods.items():
        scores=cross_validate(model,X_train,y_train,cv=cv,scoring='accuracy')
        model.fit(X_train,y_train)
        pred=model.predict(X_test)
        results[name]={'cv_accuracy_mean':round(float(scores['test_score'].mean()),4),'cv_accuracy_std':round(float(scores['test_score'].std()),4),'test_accuracy':round(float(accuracy_score(y_test,pred)),4),'confusion_matrix':confusion_matrix(y_test,pred).tolist()}
    return results

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=42);args=p.parse_args()
    print(json.dumps(benchmark(args.seed),indent=2))
if __name__=='__main__':main()
