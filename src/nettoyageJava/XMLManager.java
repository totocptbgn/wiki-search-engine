import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.io.File;
import java.io.IOException;

public class XMLManager {

    public static void load(File input, XMLStreamWriter writer, String[] theme) {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        Page.initTheme(theme);

        try {
            SAXParser parser = factory.newSAXParser();
            PageHandler pageHandler = new PageHandler(writer);
            writer.writeStartDocument("utf-8", "1.0");
            writer.writeStartElement("pages");
            parser.parse(input, pageHandler);
            writer.writeEndElement();
            writer.writeEndDocument();
        } catch (ParserConfigurationException | SAXException | IOException | XMLStreamException e) {
            throw new RuntimeException(e);
        }
    }
}
