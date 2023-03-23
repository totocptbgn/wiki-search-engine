
import java.io.*;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import static java.lang.System.currentTimeMillis;

public class CollectorMain {

    public static void main(String[] args) {
        long start = currentTimeMillis();

        if (args.length != 4) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie pour la relation mot-page] [fichier de sortie pour les IDFs] [valeur min du TF-IDF gardé]");
            return;
        }

        try {
            File input = new File(args[0]);
            TextHandler textHandler = XMLManager.load(input);
            Map<String,Float> idf = new HashMap<>();
            float numberPages = textHandler.numberPages();
            System.out.println("nombre de pages: " + numberPages);
            WordPageRelationship word_page = textHandler.getWordPageRelationships();
            System.out.println("relation mot page ok: " + word_page.size());

            Iterator<Map.Entry<String, ArrayList<PageRelation>>> iterator = word_page.entrySet().iterator();

            while (iterator.hasNext()) {
                Map.Entry<String, ArrayList<PageRelation>> wordRelations = iterator.next();
                String w = wordRelations.getKey();
                float idfW = (float) Math.log10(numberPages / word_page.get(w).size());
                ArrayList<PageRelation> wpr = wordRelations.getValue();
                for (int pr = 0; pr < wpr.size(); pr++) {
                    if (wpr.get(pr).getTF() * idfW < Float.parseFloat(args[3])) {
                        wpr.remove(wpr.get(pr));
                        if (wpr.isEmpty()) {
                            word_page.remove(w);
                        }
                    } else {
                        idf.put(w, idfW);
                    }
                }
            }

            System.out.println("relation mot page après suppressions: " + word_page.size());
            /*
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
            }*/
        } catch(ArrayIndexOutOfBoundsException | NumberFormatException e) {
            System.err.println("Arguments attendus: [fichier d'entrée] [fichier de sortie pour la relation mot-page] [fichier de sortie pour les IDFs] [valeur min du TF-IDF gardé]");
        }

        System.out.println("Temps total: " + (currentTimeMillis() - start) / 1000. + "s.");
    }
}
