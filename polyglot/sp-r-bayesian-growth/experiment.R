# Base-R sequential Bayesian conversion experiment. All data synthetic.
set.seed(42)
posterior <- function(successes, trials, prior_a=1, prior_b=1) {
 stopifnot(successes>=0, trials>=successes, prior_a>0, prior_b>0)
 c(alpha=prior_a+successes,beta=prior_b+trials-successes)
}
prob_b_wins <- function(a_success,a_total,b_success,b_total,draws=30000,seed=42){
 set.seed(seed)
 pa<-posterior(a_success,a_total);pb<-posterior(b_success,b_total)
 a<-rbeta(draws,pa[1],pa[2]);b<-rbeta(draws,pb[1],pb[2])
 list(prob_b_better=mean(b>a), expected_lift=mean(b-a), lift_interval=unname(quantile(b-a,c(.025,.975))))
}
run_demo<-function(){
 n<-8000;variant<-sample(c('control','treatment'),n,replace=TRUE)
 y<-rbinom(n,1,ifelse(variant=='control',.085,.101))
 totals<-table(variant); successes<-tapply(y,variant,sum)
 r<-prob_b_wins(successes[['control']],totals[['control']],successes[['treatment']],totals[['treatment']])
 print(r)
}
if(sys.nframe()==0)run_demo()
