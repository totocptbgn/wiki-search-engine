/*
https://stackoverflow.com/questions/26310595/how-to-parse-big-50-gb-xml-files-in-java
*/

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.io.*;
import java.util.Arrays;

import static java.lang.System.currentTimeMillis;

public class CorpusMain {

    public static void main(String[] args) {
        long start = currentTimeMillis();
        try {
            File input = new File(args[0]);
            XMLOutputFactory factory = XMLOutputFactory.newInstance();
            FileOutputStream outputStream = new FileOutputStream(args[1]);
            XMLStreamWriter writer = factory.createXMLStreamWriter(outputStream, "utf-8");
            try {
                XMLManager.load(input, writer, Arrays.copyOfRange(args, 2, args.length - 1));
            } finally {
                writer.flush();
                writer.close();
                outputStream.close();
            }
        } catch(ArrayIndexOutOfBoundsException | IllegalArgumentException e) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie] [liste non vide de mots associés au thème voulu]");
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (XMLStreamException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Temps total: " + (currentTimeMillis() - start) / 1000. + "s.");
    }
}
