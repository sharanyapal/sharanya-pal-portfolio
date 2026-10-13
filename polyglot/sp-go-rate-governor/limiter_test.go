package governor
import("testing";"time")
func TestRefillAndIsolation(t *testing.T){now:=time.Unix(0,0);l:=New(2,3,func()time.Time{return now});for i:=0;i<3;i++{if !l.Allow("a"){t.Fatal("unexpected deny")}};if l.Allow("a"){t.Fatal("burst exceeded")};if !l.Allow("b"){t.Fatal("tenants not isolated")};now=now.Add(500*time.Millisecond);if !l.Allow("a")||l.Allow("a"){t.Fatal("fractional refill incorrect")}}
func TestInvalidConfig(t *testing.T){defer func(){if recover()==nil{t.Fatal("expected panic")}}();New(0,1,time.Now)}
