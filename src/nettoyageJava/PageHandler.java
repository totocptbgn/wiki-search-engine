import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import java.io.BufferedWriter;
import java.io.IOException;

public class PageHandler extends DefaultHandler {
    private final BufferedWriter output;
    private Page page;
    private StringBuilder stringBuilder;
    private long nbPagesLues = 0;

    public PageHandler(BufferedWriter output) {
        super();
        this.output = output;
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        stringBuilder = new StringBuilder();
        if (qName.endsWith("page")) {
            page = new Page();
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.endsWith("title")) {
            page.setTitle(stringBuilder.toString());
        }else if (qName.endsWith("text")) {
            page.setText(stringBuilder.toString());
        }else if (qName.endsWith("page")) {
            try {
                page.writeOut(output);
                if (++nbPagesLues%20 == 0) {
                    System.out.println(nbPagesLues + " pages sont traitées. La dernière est " + page.getTitle() + ".");
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        stringBuilder.append(ch, start, length);
    }
}
