import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import java.util.HashMap;
import java.util.Map;

public class TextHandler extends DefaultHandler {

    private StringBuilder stringBuilder;
    private WordPageRelationship word_page;
    private int numPage = 0;

    public TextHandler() {
        word_page = new WordPageRelationship();
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        stringBuilder = new StringBuilder();
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("text")) {
            Map<String, Float> occurences = new HashMap<>();
            String[] words = stringBuilder.toString().split(" ");
            for(String w: words) {
                if (w.length() > 0) {
                    Float value = occurences.putIfAbsent(w, 1.f);
                    if (value != null) {
                        occurences.put(w, value + 1.f);
                    }
                }
            }
            word_page.addPage(numPage++, occurences);
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        stringBuilder.append(ch, start, length);
    }

    public WordPageRelationship getWordPageRelationships() {
        return word_page;
    }

    public int numberPages() {
        return numPage;
    }
}
