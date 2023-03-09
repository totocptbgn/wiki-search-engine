import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

//import java.io.BufferedWriter;
//import java.io.IOException;
import java.util.Dictionary;
import java.util.Hashtable;

public class PageHandler extends DefaultHandler {
    //private final BufferedWriter output;
    private Dictionary<String,Integer> dict = new Hashtable<>();
    private StringBuilder stringBuilder;
    private int nbTitle = 0;
    private Boolean isTitle = false;

    public PageHandler() {
        super();

    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        if (qName.equals("title")) {
            isTitle = true;
            stringBuilder = new StringBuilder();
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("title")) {
            isTitle = false;
            dict.put((stringBuilder.toString()), nbTitle);
            nbTitle++;
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        if (isTitle) {
            stringBuilder.append(ch, start, length);
        }
    }

    public Dictionary<String,Integer> getDictionary(){
        return this.dict;
    }
}
