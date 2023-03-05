import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.io.BufferedWriter;
import java.io.IOException;

public class PageHandler extends DefaultHandler {
    //private final BufferedWriter output;
    private final XMLStreamWriter writer;
    private Page page;
    private StringBuilder stringBuilder;
    private long nbPagesLues = 0;

    /*public PageHandler(BufferedWriter output) {
        super();
        this.output = output;
    }*/

    public PageHandler(XMLStreamWriter writer) {
        super();
        this.writer = writer;
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
                //page.writeOut(output);
                page.writeOut(writer);
                if (++nbPagesLues%100 == 0) {
                    System.out.println(nbPagesLues + " pages sont traitées. La dernière est " + page.getTitle() + ".");
                }
            } catch (IOException | XMLStreamException e) {
                throw new RuntimeException(e);
            }
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        stringBuilder.append(ch, start, length);
    }
}
