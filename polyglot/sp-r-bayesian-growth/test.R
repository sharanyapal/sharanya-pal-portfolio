source('experiment.R')
a<-posterior(0,10);stopifnot(a[['alpha']]==1,a[['beta']]==11)
r<-prob_b_wins(5,100,60,100,draws=5000);stopifnot(r$prob_b_better>.99)
cat('R Bayesian experiment tests passed\n')
