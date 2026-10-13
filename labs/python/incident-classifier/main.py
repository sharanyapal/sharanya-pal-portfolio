"""Tiny educational incident classification model; synthetic training examples only.
Use this as a model pipeline demonstration, never as a production decision system.
"""
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeaveOneOut, cross_val_score

EXAMPLES = {
    'identity': ['User cannot log in to corporate portal','MFA enrollment is broken','Employee account locked after password reset','Request access for new joiner','SSO authorization failed','Deprovision former employee account'],
    'network': ['Office wifi disconnected','VPN connection keeps dropping','DNS resolver unreachable','Router packet loss observed','Firewall blocks outbound traffic','Switch uplink intermittent'],
    'application': ['Web dashboard returns server error','App crashes on submitting form','Database query timeout on reports','API endpoint returns 500','ServiceNow catalog form fails to submit','UI button not working'],
    'hardware': ['Laptop battery will not charge','Monitor screen has dead pixels','Keyboard keys are stuck','SSD device not detected','Computer overheats under load','Printer paper jam']
}

def model():
    X=[sample for examples in EXAMPLES.values() for sample in examples]
    y=[label for label,examples in EXAMPLES.items() for _ in examples]
    pipe=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2))),('classifier',LogisticRegression(max_iter=1000,random_state=7))])
    pipe.fit(X,y)
    return pipe,X,y

def predict(text:str)->dict:
    pipe,_,_=model()
    probabilities=pipe.predict_proba([text])[0]
    ranked=sorted(zip(pipe.classes_,probabilities),key=lambda item:item[1],reverse=True)
    return {'category':ranked[0][0],'confidence':round(float(ranked[0][1]),3),'scores':{k:round(float(v),3) for k,v in ranked},'note':'Synthetic small-data demo; low confidence expected'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('incident',nargs='?',default='New employee cannot access SSO')
    p.add_argument('--evaluate',action='store_true')
    args=p.parse_args()
    if args.evaluate:
        clf,X,y=model()
        score=cross_val_score(clf,X,y,cv=LeaveOneOut())
        print(f'Leave-one-out accuracy on synthetic sample: {score.mean():.2%} ({len(X)} cases)')
    else:
        import json
        print(json.dumps(predict(args.incident),indent=2))

if __name__=='__main__':main()
