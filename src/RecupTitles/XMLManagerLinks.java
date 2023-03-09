import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.SAXException;

import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;


public class XMLManagerLinks {
    public static void load(File input, BufferedWriter writer, HashMap<String,Integer> dict) throws ParserConfigurationException, SAXException, IOException{

        SAXParserFactory factory = SAXParserFactory.newInstance();

        SAXParser parser = factory.newSAXParser();
        LinksHandler linksHandler = new LinksHandler(writer, dict);
        parser.parse(input, linksHandler);


    }

}