import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
//import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;

public class XMLManager {
    public static HashMap<String,Integer> load(File input) throws ParserConfigurationException, SAXException, IOException{

        SAXParserFactory factory = SAXParserFactory.newInstance();

        SAXParser parser = factory.newSAXParser();
        PageHandler pageHandler = new PageHandler();
        parser.parse(input, pageHandler);
        return pageHandler.getHashMap();
        /*try {
            SAXParser parser = factory.newSAXParser();
            PageHandler pageHandler = new PageHandler();
            parser.parse(input, pageHandler);
            return pageHandler.getHashMap();

        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }*/

    }

}