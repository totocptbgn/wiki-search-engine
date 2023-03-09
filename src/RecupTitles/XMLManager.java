import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
//import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.Dictionary;

public class XMLManager {
    public static Dictionary<String,Integer> load(File input) throws ParserConfigurationException, SAXException, IOException{

        SAXParserFactory factory = SAXParserFactory.newInstance();

        SAXParser parser = factory.newSAXParser();
        PageHandler pageHandler = new PageHandler();
        parser.parse(input, pageHandler);
        return pageHandler.getDictionary();
        /*try {
            SAXParser parser = factory.newSAXParser();
            PageHandler pageHandler = new PageHandler();
            parser.parse(input, pageHandler);
            return pageHandler.getDictionary();

        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }*/

    }

}