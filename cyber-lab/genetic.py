"""Genetic algorithm demo optimizing a toy threshold; not a security detector."""
import random
def evolve_threshold(generations=30):
    random.seed(13); data=[(i/100,int(i/100>=.65)) for i in range(101)]; pop=[random.random() for _ in range(24)]
    def fitness(t): return sum(int((x>=t)==bool(y)) for x,y in data)/len(data)
    history=[]
    for _ in range(generations):
        pop.sort(key=fitness,reverse=True); history.append(round(fitness(pop[0]),4)); nxt=pop[:4]
        while len(nxt)<24: nxt.append(min(1,max(0,random.choice(pop[:10])+random.gauss(0,.08))))
        pop=nxt
    best=max(pop,key=fitness)
    return {"best_threshold":round(best,4),"fitness":round(fitness(best),4),"generations":generations,"history":history,"warning":"Toy optimization only; not a vulnerability detector."}
