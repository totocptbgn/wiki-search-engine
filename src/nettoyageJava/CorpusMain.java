/*
https://stackoverflow.com/questions/26310595/how-to-parse-big-50-gb-xml-files-in-java
*/

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

import static java.lang.System.currentTimeMillis;

public class CorpusMain {

    public static void main(String[] args) {
        long start = currentTimeMillis();
        try {
            File input = new File(args[0]);
            FileWriter outputWriter = new FileWriter(args[1]);
            BufferedWriter outputBW = new BufferedWriter(outputWriter);
            XMLManager.load(input, outputBW, Arrays.copyOfRange(args, 2, args.length-1));
            outputBW.close();
        } catch(ArrayIndexOutOfBoundsException | IllegalArgumentException e) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie] [liste non vide de mots associés au thème voulu]");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Temps total: " + (currentTimeMillis() - start) / 1000. + "s.");
    }
}
