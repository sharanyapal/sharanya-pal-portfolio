package governor
import("sync";"time")
type Bucket struct{Tokens float64; Updated time.Time}
type Limiter struct{mu sync.Mutex; clients map[string]*Bucket; rate,capacity float64; now func()time.Time}
func New(rate,burst float64,clock func()time.Time)*Limiter{if rate<=0||burst<1{panic("invalid rate")};return &Limiter{clients:make(map[string]*Bucket),rate:rate,capacity:burst,now:clock}}
func(l *Limiter) Allow(client string)bool{l.mu.Lock();defer l.mu.Unlock();t:=l.now();b,ok:=l.clients[client];if !ok{b=&Bucket{Tokens:l.capacity,Updated:t};l.clients[client]=b};elapsed:=t.Sub(b.Updated).Seconds();if elapsed>0{b.Tokens=min(l.capacity,b.Tokens+elapsed*l.rate);b.Updated=t};if b.Tokens<1{return false};b.Tokens--;return true}
// Cleanup removes idle clients so the key-space doesn't grow forever.
func(l *Limiter) Cleanup(idle time.Duration){l.mu.Lock();defer l.mu.Unlock();t:=l.now();for k,b:=range l.clients{if t.Sub(b.Updated)>idle{delete(l.clients,k)}}}
