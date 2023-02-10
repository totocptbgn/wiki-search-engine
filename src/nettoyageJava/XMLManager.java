import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;

public class XMLManager {
    public static void load(File input, BufferedWriter output, String[] theme) {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        Page.initTheme(theme);

        try {
            SAXParser parser = factory.newSAXParser();
            PageHandler pageHandler = new PageHandler(output);
            output.write("<pages>");
            parser.parse(input, pageHandler);
            output.write("</pages>");
        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }
    }
}
