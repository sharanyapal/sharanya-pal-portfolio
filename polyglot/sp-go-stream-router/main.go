package main
import("encoding/json";"fmt";"log";"net/http";"sync";"time";"math")
type Event struct{ At time.Time `json:"at"`; Source string `json:"source"`; Latency float64 `json:"latency_ms"`; Status int `json:"status"` }
type Alert struct{Source string `json:"source"`; Count int `json:"count"`; At time.Time `json:"at"`}
type Detector struct{mu sync.Mutex; bySource map[string][]time.Time; window time.Duration; threshold int}
func NewDetector(window time.Duration, threshold int)*Detector{return &Detector{bySource:make(map[string][]time.Time),window:window,threshold:threshold}}
func (d *Detector) Ingest(e Event)*Alert{d.mu.Lock();defer d.mu.Unlock();if e.Status<500{return nil};times:=d.bySource[e.Source][:0];for _,t:=range d.bySource[e.Source]{if !t.Before(e.At.Add(-d.window)) && !t.After(e.At){times=append(times,t)}};times=append(times,e.At);d.bySource[e.Source]=times;if len(times)>=d.threshold{return &Alert{e.Source,len(times),e.At}};return nil}
type Bus struct {mu sync.Mutex; clients map[chan []byte]struct{}}
func (b *Bus) register(c chan []byte){b.mu.Lock();b.clients[c]=struct{}{};b.mu.Unlock()}
func (b *Bus) unregister(c chan []byte){b.mu.Lock();delete(b.clients,c);close(c);b.mu.Unlock()}
func (b *Bus) publish(data []byte){b.mu.Lock();defer b.mu.Unlock();for c:=range b.clients{select{case c<-data:default: /* drop for slow subscriber, never block producer */}}}
func main(){detector:=NewDetector(15*time.Second,3);bus:=&Bus{clients:make(map[chan []byte]struct{})};incoming:=make(chan Event,128)
 go func(){for e:=range incoming{payload,_:=json.Marshal(e);bus.publish(payload);if a:=detector.Ingest(e);a!=nil{log.Printf("ALERT source=%s count=%d",a.Source,a.Count)}}}()
 http.HandleFunc("/healthz",func(w http.ResponseWriter,r *http.Request){w.Header().Set("Content-Type","application/json");fmt.Fprint(w,`{"healthy":true,"mode":"local-demo"}`)})
 http.HandleFunc("/events",func(w http.ResponseWriter,r *http.Request){w.Header().Set("Content-Type","text/event-stream");w.Header().Set("Cache-Control","no-cache");w.Header().Set("X-Content-Type-Options","nosniff");f,ok:=w.(http.Flusher);if !ok{http.Error(w,"streaming unavailable",500);return};client:=make(chan []byte,32);bus.register(client);defer bus.unregister(client);for{select{case data:=<-client:fmt.Fprintf(w,"data: %s\n\n",data);f.Flush();case <-r.Context().Done():return}}})
 // Local-only simulator: this example never reads real production logs.
 go func(){tick:=time.NewTicker(200*time.Millisecond);defer tick.Stop();i:=0;for t:=range tick.C{i++;e:=Event{At:t,Source:[]string{"iam","api","catalog"}[i%3],Latency:90+50*math.Sin(float64(i)/7),Status:200};if i%17<3{e.Status=503};select{case incoming<-e:default:}}}()
 fmt.Println("SSE telemetry at http://127.0.0.1:8088/events");log.Fatal(http.ListenAndServe("127.0.0.1:8088",nil))
}
