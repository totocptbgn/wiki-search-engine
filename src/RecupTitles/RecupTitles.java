//import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
//import java.io.FileWriter;
import java.util.Dictionary;

import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

public class RecupTitles {
    public static void main(String[] args) {
        try {
            File input = new File(args[0]);
            //FileWriter outputWriter = new FileWriter(args[1]);
            //BufferedWriter outputBW = new BufferedWriter(outputWriter);
            Dictionary<String,Integer> dict = XMLManager.load(input);
            System.out.println(dict);
            System.out.println("Le dictionnaire contient " + dict.size() + " titres.");
            //outputBW.close();
        } catch (IOException e) {
            // TODO: handle exception
            System.out.println("COUCOU");
        } catch (SAXException e) {
            System.out.println("Sax");
            e.printStackTrace();
        }
        catch (ParserConfigurationException e) {
            System.out.println("Parser");
        }
        
    }
}
