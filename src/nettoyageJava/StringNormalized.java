import java.text.Normalizer;
import java.util.regex.Pattern;

public class StringNormalized {

    private final static Pattern carSpeciauxPattern = Pattern.compile("[^a-z ]");
    private final static Pattern seulePattern = Pattern.compile(" infobox | px | [a-z] ");
    private final static Pattern simpleEspacePattern = Pattern.compile(" +");

    public static String normalize(String str) {
        str = str.toLowerCase();
        str = Normalizer.normalize(str, Normalizer.Form.NFKD)
                .replaceAll("\\p{M}", "");
        str = carSpeciauxPattern.matcher(str).replaceAll(" ");
        str = seulePattern.matcher(str).replaceAll(" ");
        return simpleEspacePattern.matcher(str).replaceAll(" ");
    }
}
