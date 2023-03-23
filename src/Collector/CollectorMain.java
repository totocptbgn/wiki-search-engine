
import java.io.*;
import java.util.HashMap;
import java.util.Map;

import static java.lang.System.currentTimeMillis;

public class CollectorMain {

    public static void main(String[] args) {
        long start = currentTimeMillis();

        if (args.length != 3) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie pour la relation mot-page] [fichier de sortie pour les IDFs]");
            return;
        }

        try {
            File input = new File(args[0]);
            TextHandler textHandler = XMLManager.load(input);
            Map<String,Float> idf = new HashMap<>();
            float numberPages = textHandler.numberPages();
            System.out.println("nombre de pages: " + numberPages);
            WordPageRelationship word_page = textHandler.getWordPageRelationships();
            for (String w: word_page.keySet()) {
                System.out.println(w);
                idf.put(w, (float) Math.log10(numberPages / word_page.get(w).size()));
            }
            try {
                ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(args[1]));
                oos.writeObject(word_page);
                oos.close();
            } catch (IOException e) {
                System.err.println("Impossible de sérialiser la relation mot-page: " + e);
            }
            try {
                ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(args[2]));
                oos.writeObject(word_page);
                oos.close();
            } catch (IOException e) {
                System.err.println("Impossible de sérialiser les IDFs des mots: " + e);
            }
        } catch(ArrayIndexOutOfBoundsException e) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie pour la relation mot-page] [fichier de sortie pour les IDFs]");
        }

        System.out.println("Temps total: " + (currentTimeMillis() - start) / 1000. + "s.");
    }
}
