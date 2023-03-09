import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.FileWriter;
import java.util.HashMap;

import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

public class RecupTitles {
    public static void main(String[] args) {
        try {
            File input = new File(args[0]);
            HashMap<String,Integer> dict = XMLManager.load(input);
            System.out.println("Le dictionnaire contient " + dict.size() + " titres.");
            FileWriter outputWriter = new FileWriter(args[1]);
            BufferedWriter outputBW = new BufferedWriter(outputWriter);
            try {
            XMLManagerLinks.load(input, outputBW, dict);

            } finally {
                outputBW.flush();
                outputBW.close();
                outputWriter.close();
            }

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
