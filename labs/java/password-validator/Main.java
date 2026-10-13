import java.util.*;

/** Password policy evaluator with actionable, non-sensitive feedback.
 * It intentionally never logs or stores the supplied password.
 */
public class Main {
    record Review(boolean valid, List<String> recommendations) {}
    static Review review(String password) {
        List<String> issues=new ArrayList<>();
        if (password.length()<14) issues.add("Use 14 or more characters");
        if (password.chars().noneMatch(Character::isUpperCase)) issues.add("Include an uppercase letter");
        if (password.chars().noneMatch(Character::isLowerCase)) issues.add("Include a lowercase letter");
        if (password.chars().noneMatch(Character::isDigit)) issues.add("Include a digit");
        if (password.chars().noneMatch(c->!Character.isLetterOrDigit(c))) issues.add("Include a symbol");
        if (password.toLowerCase(Locale.ROOT).contains("password")) issues.add("Avoid obvious phrases");
        return new Review(issues.isEmpty(),List.copyOf(issues));
    }
    public static void main(String[] args) {
        if (args.length>0 && args[0].equals("--self-test")) {
            assert review("N3on-Adventure!2026").valid();
            assert !review("password123").valid();
            System.out.println("PASS: password policy tests");return;
        }
        System.out.println("Password Policy Validator");
        System.out.println("Safe demonstration with an example string (no real credentials required)");
        Review result=review("Demo-String123!");
        System.out.println("Valid: " + result.valid());
        result.recommendations().forEach(r->System.out.println(" - " + r));
    }
}
