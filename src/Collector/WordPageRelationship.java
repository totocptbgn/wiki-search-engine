import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class WordPageRelationship extends HashMap<String, ArrayList<PageRelation>> implements Serializable {

    public void addPage(int numPage, Map<String, Float> occurences) {
        double Nd = 0.;
        for (String word: occurences.keySet()) {
            double tf = 1. + Math.log10(occurences.get(word));
            occurences.put(word, (float) tf);
            Nd += tf * tf;
        }
        Nd = Math.sqrt(Nd);
        Set<String> pageKeys = keySet();
        for (String word: occurences.keySet()) {
            if (pageKeys.contains(word)) {
                get(word).add(new PageRelation(numPage, occurences.get(word) / (float) Nd));
            } else {
                ArrayList<PageRelation> firstFound = new ArrayList<>();
                firstFound.add(new PageRelation(numPage, occurences.get(word) / (float) Nd));
                put(word, firstFound);
            }
        }
    }
}
