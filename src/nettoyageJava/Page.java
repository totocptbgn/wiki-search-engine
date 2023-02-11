import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Page {
    private String title;
    private String text;
    private final ArrayList<String> liens;
    private static final Pattern lienPattern = Pattern.compile("\\[\\[(?!Fichier:|File:|Catégorie:|Category:|#)(.+?)(#(.+?))?(\\|(.+?))?\\]\\]");
    private static final Pattern refPattern = Pattern.compile("(<ref(.+?)</ref>)|(<ref (.+?)/>)");
    private static final Pattern sectionPattern = Pattern.compile("=== (.+?) ===");
    private static final Pattern externePattern = Pattern.compile("\\{\\{(.+?)\\}\\}");
    private static final Pattern margePattern = Pattern.compile("(border-right|border-bottom|margin-top)(.+?)(;|\\n)");
    private static final Pattern stylePattern = Pattern.compile("(style|align|class|width|colspan|rowspan|float|maxvalue|bg|border|barcolor|scope|rules|cellspacing|cellpadding|bgcolor)(\\s*)=(.+?)(\\s|\\|)");
    private static final Pattern colorPattern = Pattern.compile("color:(\\s*)(#|\\w)(\\w+)");
    private static final Pattern filePattern = Pattern.compile("\\[\\[(Fichier:|File:|Catégorie:|Category:)(.+?)\\]\\]");
    private static final Pattern galleryPattern = Pattern.compile("(?s)<gallery(.+?)</gallery>");
    private static final Pattern balisePattern = Pattern.compile("<(.+?)>");
    private static final Pattern internePattern = Pattern.compile("\\s\\[[^\\[](.+?)[^\\]]\\]\\s");
    private static final Pattern colonnePattern = Pattern.compile("\\{\\{colonnes|nombre=\\d");
    private static Pattern themePattern;
    private final static int lenMin = 1000 * 6; // minimum de 1000 mots, si on compte qu'un mot fait en moyenne 5 lettres + espaces

    public Page() {
        this.liens = new ArrayList<>();
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setText(String text) {
        this.text = text;
    }

    public static void initTheme(String[] theme) {
        // TODO verifier regex
        Page.themePattern = Pattern.compile("[^A-Za-z]" + String.join("[^A-Za-z]|[^A-Za-z]", theme) + "[^A-Za-z]");
    }

    private boolean toWrite() {
        return Page.themePattern.matcher(text).find();
    }

    public void writeOut(BufferedWriter output) throws IOException {
        if (toWrite()) {
            processLiens();
            if (processText()) {
                output.write(toString());
            }
        }
    }

    private boolean processText() {
        // TODO verifier regex
        text = refPattern.matcher(text).replaceAll(" ");
        text = sectionPattern.matcher(text).replaceAll(" ");
        text = externePattern.matcher(text).replaceAll(" ");
        text = margePattern.matcher(text).replaceAll(" ");
        text = stylePattern.matcher(text).replaceAll(" ");
        text = colorPattern.matcher(text).replaceAll(" ");
        text = filePattern.matcher(text).replaceAll(" ");
        text = galleryPattern.matcher(text).replaceAll(" ");
        text = balisePattern.matcher(text).replaceAll(" ");
        text = internePattern.matcher(text).replaceAll(" ");
        text = colonnePattern.matcher(text).replaceAll(" ");
        text = StringNormalized.normalize(text);

        return text.length() >= lenMin;
    }

    private void processLiens() {
        Matcher matcher = Page.lienPattern.matcher(text);
        while (matcher.find()) {
            liens.add(matcher.group(1));
        }
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("<page><title>");
        builder.append(title);
        builder.append("</title><text>");
        builder.append(text);
        builder.append("</text><links>");
        for (String lien: liens) {
            builder.append(lien);
            builder.append("\n");
        }
        builder.append("</links></page>");
        return builder.toString();
    }
}