
import java.io.*;
import java.util.*;

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

            Iterator<Map.Entry<String, ArrayList<PageRelation>>> wordIterator = word_page.entrySet().iterator();

            while (wordIterator.hasNext()) {
                Map.Entry<String, ArrayList<PageRelation>> wordRelations = wordIterator.next();
                String w = wordRelations.getKey();
                ArrayList<PageRelation> wpr = wordRelations.getValue();
                float idfW = (float) Math.log10(numberPages / wpr.size());
                Iterator<PageRelation> pageIterator = wpr.iterator();
                while (pageIterator.hasNext()) {
                    PageRelation pr = pageIterator.next();
                    if (pr.getTF() * idfW < Float.parseFloat(args[3])) {
                        pageIterator.remove();
                        if (wpr.isEmpty()) {
                            wordIterator.remove();
                        }
                    } else {
                        idf.put(w, idfW);
                    }
                }
            }

            System.out.println("relation mot page après suppressions: " + word_page.size());

            double moy = 0.;
            int max = 0;
            String mostCommon = null;
            int min = 1000;
            String lessCommon = null;
            for (Map.Entry<String, ArrayList<PageRelation>> wordRelations: word_page.entrySet()) {
                int size = wordRelations.getValue().size();
                moy += size;
                if (size > max) {
                    max = size;
                    mostCommon = wordRelations.getKey();
                }
                if (size < min) {
                    min = size;
                    lessCommon = wordRelations.getKey();
                }
            }

            System.out.println("moyenne nombre de pages par mot: " + (moy / numberPages));
            System.out.println("nombre max de pages contenant un mot: " + max + " pour le mot " + mostCommon);
            System.out.println("nombre min de pages contenant un mot: " + min + " pour le mot " + lessCommon);

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
