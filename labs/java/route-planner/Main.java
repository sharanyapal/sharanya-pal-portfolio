import java.util.*;

/** Dijkstra shortest path using adjacency lists and a min-priority queue. */
public class Main {
    record Edge(String to, int cost) { }
    record State(String vertex, int distance) { }
    record Path(int distance, List<String> vertices) { }
    private final Map<String, List<Edge>> graph = new HashMap<>();
    void connect(String from, String to, int weight) {
        if (weight < 0) throw new IllegalArgumentException("Negative edge weight not supported");
        graph.computeIfAbsent(from,k->new ArrayList<>()).add(new Edge(to,weight));
        graph.putIfAbsent(to,new ArrayList<>());
    }
    Path shortest(String start, String goal) {
        Map<String,Integer> distances = new HashMap<>();
        Map<String,String> previous = new HashMap<>();
        PriorityQueue<State> queue = new PriorityQueue<>(Comparator.comparingInt(State::distance));
        distances.put(start,0); queue.add(new State(start,0));
        while (!queue.isEmpty()) {
            State current = queue.poll();
            if (current.distance != distances.getOrDefault(current.vertex,Integer.MAX_VALUE)) continue;
            if (current.vertex.equals(goal)) break;
            for (Edge edge:graph.getOrDefault(current.vertex,List.of())) {
                int candidate = current.distance + edge.cost();
                if (candidate < distances.getOrDefault(edge.to(),Integer.MAX_VALUE)) {
                    distances.put(edge.to(),candidate); previous.put(edge.to(),current.vertex);
                    queue.add(new State(edge.to(),candidate));
                }
            }
        }
        if (!distances.containsKey(goal)) return new Path(-1,List.of());
        List<String> route = new ArrayList<>();
        for (String node=goal;node!=null;node=previous.get(node)) route.add(node);
        Collections.reverse(route);
        return new Path(distances.get(goal),route);
    }
    public static void main(String[] args) {
        Main routes = new Main();
        routes.connect("Station","Library",4);routes.connect("Station","Park",2);
        routes.connect("Park","Library",1);routes.connect("Library","Office",3);
        routes.connect("Park","Office",10);routes.connect("Office","Cafe",2);
        Path result=routes.shortest("Station","Cafe");
        if (args.length>0 && args[0].equals("--self-test")) {
            assert result.distance()==8 : result;
            assert result.vertices().equals(List.of("Station","Park","Library","Office","Cafe"));
            assert routes.shortest("Cafe","Station").distance()==-1;
            System.out.println("PASS: Dijkstra tests");return;
        }
        System.out.println("Shortest path: " + String.join(" -> ",result.vertices()));
        System.out.println("Total edge cost: " + result.distance());
    }
}
