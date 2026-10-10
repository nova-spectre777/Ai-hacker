"""Tiny NumPy network trained by backpropagation on synthetic teaching data.
This is a learning-mechanics demo, not a cybersecurity classifier."""
import numpy as np
X=np.array([[0,0],[0,1],[1,0],[1,1],[.1,.2],[.2,.9],[.9,.2],[.9,.9],[.05,.95],[.95,.05],[.8,.8],[.1,.1]],float)
Y=np.array([[0],[1],[0],[1],[0],[1],[0],[1],[1],[0],[1],[0]],float)
MODEL=None
def sigmoid(x): return 1/(1+np.exp(-np.clip(x,-40,40)))
def train_demo(epochs=80):
    global MODEL
    rng=np.random.default_rng(7); w1=rng.normal(0,.7,(2,4)); b1=np.zeros((1,4)); w2=rng.normal(0,.7,(4,1)); b2=np.zeros((1,1)); losses=[]
    for _ in range(epochs):
        a1=np.tanh(X@w1+b1); p=sigmoid(a1@w2+b2); eps=1e-7
        loss=-np.mean(Y*np.log(p+eps)+(1-Y)*np.log(1-p+eps)); losses.append(round(float(loss),5))
        dz2=(p-Y)/len(X); dw2=a1.T@dz2; db2=dz2.sum(axis=0,keepdims=True)
        dz1=(dz2@w2.T)*(1-a1*a1); dw1=X.T@dz1; db1=dz1.sum(axis=0,keepdims=True)
        w2-=.8*dw2; b2-=.8*db2; w1-=.8*dw1; b1-=.8*db1
    MODEL=(w1,b1,w2,b2)
    return {"message":"Real backpropagation completed on synthetic teaching data.","epochs":epochs,"initial_loss":losses[0],"final_loss":losses[-1],"losses":losses,"warning":"This toy model does not discover vulnerabilities; it demonstrates the training process."}
def predict_demo(features):
    global MODEL
    if MODEL is None: train_demo(80)
    w1,b1,w2,b2=MODEL; x=np.array([features],float); score=float(sigmoid(np.tanh(x@w1+b1)@w2+b2)[0,0])
    return {"score":round(score,4),"label":"higher toy score" if score>=.5 else "lower toy score","warning":"Not a real vulnerability probability. Do not use for security decisions."}
