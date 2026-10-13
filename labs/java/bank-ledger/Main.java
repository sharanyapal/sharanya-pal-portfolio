import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

/** Educational ledger: decimal precision, non-negative balances, transfer audit trail. */
public class Main {
    static class Ledger {
        private final Map<String, BigDecimal> balance = new LinkedHashMap<>();
        private final List<String> events = new ArrayList<>();
        private static BigDecimal money(String value) {
            BigDecimal amount = new BigDecimal(value).setScale(2, RoundingMode.UNNECESSARY);
            if (amount.signum() <= 0) throw new IllegalArgumentException("Amount must be positive");
            return amount;
        }
        synchronized void create(String account, String initial) {
            if (balance.containsKey(account)) throw new IllegalArgumentException("Account exists");
            BigDecimal amount = new BigDecimal(initial).setScale(2, RoundingMode.UNNECESSARY);
            if (amount.signum() < 0) throw new IllegalArgumentException("Negative opening balance");
            balance.put(account, amount); events.add("OPEN:" + account + ":" + amount);
        }
        synchronized void transfer(String from, String to, String amountText) {
            BigDecimal amount = money(amountText);
            if (from.equals(to)) throw new IllegalArgumentException("Cannot transfer to self");
            if (!balance.containsKey(from) || !balance.containsKey(to)) throw new IllegalArgumentException("Account not found");
            if (balance.get(from).compareTo(amount) < 0) throw new IllegalArgumentException("Insufficient funds");
            balance.put(from, balance.get(from).subtract(amount));
            balance.put(to, balance.get(to).add(amount));
            events.add("TRANSFER:" + from + ":" + to + ":" + amount);
        }
        synchronized BigDecimal get(String id) { return balance.get(id); }
        synchronized List<String> audit() { return List.copyOf(events); }
    }
    public static void main(String[] args) {
        Ledger ledger = new Ledger();
        ledger.create("alice", "500.00"); ledger.create("bob", "90.00");
        ledger.transfer("alice", "bob", "124.75");
        if (args.length > 0 && args[0].equals("--self-test")) {
            assert ledger.get("alice").compareTo(new BigDecimal("375.25")) == 0;
            assert ledger.get("bob").compareTo(new BigDecimal("214.75")) == 0;
            boolean refused = false;
            try { ledger.transfer("alice", "bob", "90000"); } catch (IllegalArgumentException ex) { refused = true; }
            assert refused : "Overdraft should have been refused";
            System.out.println("PASS: ledger invariant tests"); return;
        }
        System.out.println("Account balances:");
        System.out.println("alice = " + ledger.get("alice") + ", bob = " + ledger.get("bob"));
        System.out.println("Audit:"); ledger.audit().forEach(System.out::println);
    }
}
