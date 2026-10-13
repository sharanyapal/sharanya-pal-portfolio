source('risk.R')
x<-matrix(c(-.2,.1,.02,-.03,.08,.04,.11,-.1),ncol=2);r<-risk_report(x,c(.5,.5),boot=50)
stopifnot(r$ExpectedShortfall>=r$VaR,is.finite(r$annualized_vol))
cat('R risk tests passed\n')
