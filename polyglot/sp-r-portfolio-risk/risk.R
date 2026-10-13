# Diversified portfolio VaR and expected shortfall with bootstrap confidence intervals.
portfolio_losses <- function(returns,weights){
 stopifnot(is.matrix(returns),ncol(returns)==length(weights),abs(sum(weights)-1)<1e-9,all(is.finite(returns)))
 -as.vector(returns %*% weights)
}
risk_report<-function(returns,weights,alpha=.95,boot=300,seed=9){
 stopifnot(alpha>.5,alpha<1,boot>10)
 losses<-portfolio_losses(returns,weights)
 var<-as.numeric(quantile(losses,alpha));es<-mean(losses[losses>=var])
 set.seed(seed);v<-replicate(boot,as.numeric(quantile(sample(losses,replace=TRUE),alpha)))
 list(VaR=var,ExpectedShortfall=es,VaR_bootstrap_CI=unname(quantile(v,c(.025,.975))),annualized_vol=sd(losses)*sqrt(252))
}
if(sys.nframe()==0){
 set.seed(17); z<-matrix(rnorm(7500,0,.017),ncol=3); z[,2]<-z[,2]*.7+z[,1]*.3
 print(risk_report(z,c(.45,.35,.20)))
}
