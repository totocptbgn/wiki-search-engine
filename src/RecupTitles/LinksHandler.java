import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;
import java.io.BufferedWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

public class LinksHandler extends DefaultHandler {
    private final BufferedWriter output;
    private StringBuilder stringBuilderRecup;
    private Boolean isLinks = false;
    private HashMap<String,Integer> dict;
    public LinksHandler(BufferedWriter output, HashMap<String,Integer> dict) {
        super();
        this.output = output;
        this.dict = dict;
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        if (qName.equals("links")) {
            isLinks = true;
            stringBuilderRecup = new StringBuilder();
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("links")) {
            StringBuilder stringBuilderVerif = new StringBuilder();
            isLinks = false;
            String[] linksPage = stringBuilderRecup.toString().split("\n");
            Set<String> set = new HashSet<>();
            set.addAll(Arrays.asList(linksPage));
            for (String s: set){
                Integer value = dict.get(s);
                if (value != null){
                    stringBuilderVerif.append(value);
                    stringBuilderVerif.append(",");
                }
            }
            stringBuilderVerif.append("\n");
            try {
                output.write(stringBuilderVerif.toString());
            }

            catch (IOException e){
                throw new RuntimeException(e);
            }
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        if (isLinks) {
            stringBuilderRecup.append(ch, start, length);
        }
    }
}
