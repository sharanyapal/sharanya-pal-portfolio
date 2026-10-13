package main
import("testing";"time")
func TestDetector(t *testing.T){d:=NewDetector(10*time.Second,3);start:=time.Date(2026,1,1,0,0,0,0,time.UTC);for i:=0;i<2;i++{if d.Ingest(Event{At:start.Add(time.Duration(i)*time.Second),Source:"auth",Status:503})!=nil{t.Fatal("premature alert")}};if a:=d.Ingest(Event{At:start.Add(2*time.Second),Source:"auth",Status:500});a==nil||a.Count!=3{t.Fatal("expected alert")};if a:=d.Ingest(Event{At:start.Add(30*time.Second),Source:"auth",Status:503});a!=nil{t.Fatal("window should expire")}}
func TestDropSlowSubscriber(t *testing.T){b:=&Bus{clients:make(map[chan []byte]struct{})};c:=make(chan []byte,1);b.register(c);b.publish([]byte("first"));b.publish([]byte("second"));if string(<-c)!="first"{t.Fatal("expected bounded queue")};b.unregister(c)}
