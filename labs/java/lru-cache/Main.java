import java.util.*;

/** Generic bounded LRU cache based on an access-order LinkedHashMap. */
public class Main {
    static class LRUCache<K,V> {
        private final int capacity;
        private final LinkedHashMap<K,V> map;
        LRUCache(int capacity) {
            if (capacity < 1) throw new IllegalArgumentException("Capacity must be positive");
            this.capacity=capacity;
            this.map=new LinkedHashMap<>(16,.75f,true);
        }
        synchronized V get(K key) { return map.get(key); }
        synchronized void put(K key,V value) {
            map.put(key,value);
            if (map.size()>capacity) map.remove(map.keySet().iterator().next());
        }
        synchronized Map<K,V> snapshot() { return new LinkedHashMap<>(map); }
    }
    public static void main(String[] args) {
        LRUCache<Integer,String> cache=new LRUCache<>(3);
        cache.put(1,"Identity");cache.put(2,"ServiceNow");cache.put(3,"Python");
        cache.get(1);cache.put(4,"Java");
        if (args.length>0 && args[0].equals("--self-test")) {
            assert cache.get(2)==null : "Least recently used key was not evicted";
            assert "Identity".equals(cache.get(1));
            assert cache.snapshot().size()==3;
            System.out.println("PASS: cache eviction tests");return;
        }
        System.out.println("Most recently used cache entries: " + cache.snapshot());
    }
}
