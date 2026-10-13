import java.util.*;
/** Self-contained price-time priority limit order matching engine; no external dependencies. */
public class MatchingEngine {
    public enum Side { BUY, SELL }
    public record Trade(long buyOrderId,long sellOrderId,long priceCents,long quantity) {}
    public static final class Order {
        public final long id,priceCents;public long remaining;
        public final Side side;public final long receivedAt;
        public Order(long id,Side side,long priceCents,long quantity,long receivedAt){
            if(id<=0||priceCents<=0||quantity<=0)throw new IllegalArgumentException("Price, quantity, id must be positive");
            this.id=id;this.side=side;this.priceCents=priceCents;this.remaining=quantity;this.receivedAt=receivedAt;
        }
    }
    private final NavigableMap<Long,Deque<Order>> bids=new TreeMap<>(Comparator.reverseOrder());
    private final NavigableMap<Long,Deque<Order>> asks=new TreeMap<>();
    private final Map<Long,Order> live=new HashMap<>();
    private long tick=0;
    public synchronized List<Trade> submit(long id,Side side,long priceCents,long quantity){
        if(live.containsKey(id))throw new IllegalArgumentException("Duplicate open order ID");
        Order incoming=new Order(id,side,priceCents,quantity,++tick);
        var opposite=side==Side.BUY?asks:bids;
        var own=side==Side.BUY?bids:asks;
        List<Trade> trades=new ArrayList<>();
        while(incoming.remaining>0&&!opposite.isEmpty()){
            long best=opposite.firstKey();
            if((side==Side.BUY&&priceCents<best)||(side==Side.SELL&&priceCents>best))break;
            Deque<Order> level=opposite.firstEntry().getValue();
            Order resting=level.peekFirst();
            long filled=Math.min(incoming.remaining,resting.remaining);
            trades.add(new Trade(side==Side.BUY?id:resting.id,side==Side.SELL?id:resting.id,
                                 resting.priceCents,filled));
            incoming.remaining-=filled;resting.remaining-=filled;
            if(resting.remaining==0){level.removeFirst();live.remove(resting.id);if(level.isEmpty())opposite.pollFirstEntry();}
        }
        if(incoming.remaining>0){own.computeIfAbsent(priceCents,unused->new ArrayDeque<>()).addLast(incoming);live.put(id,incoming);}
        return trades;
    }
    public synchronized boolean cancel(long id){
        Order o=live.remove(id);if(o==null)return false;
        var book=o.side==Side.BUY?bids:asks;
        Deque<Order> q=book.get(o.priceCents);q.remove(o);if(q.isEmpty())book.remove(o.priceCents);
        return true;
    }
    public synchronized String bestBidAsk(){
        return "Bid "+(bids.isEmpty()?"empty":bids.firstKey())+" / Ask "+(asks.isEmpty()?"empty":asks.firstKey());
    }
    public static void main(String[] args){
        MatchingEngine m=new MatchingEngine();
        assert m.submit(1,Side.SELL,10250,4).isEmpty();
        assert m.submit(2,Side.SELL,10250,3).isEmpty();
        List<Trade> trades=m.submit(3,Side.BUY,10400,6);
        assert trades.size()==2:"One incoming buy matches two resting sells";
        assert trades.get(0).sellOrderId()==1&&trades.get(0).quantity()==4;
        assert trades.get(1).sellOrderId()==2&&trades.get(1).quantity()==2;
        assert m.cancel(2);
        assert !m.cancel(2);
        assert m.submit(4,Side.SELL,10100,2).isEmpty();
        assert m.submit(5,Side.BUY,10100,2).get(0).priceCents()==10100;
        System.out.println("6 matching engine invariants passed; "+m.bestBidAsk());
    }
}
