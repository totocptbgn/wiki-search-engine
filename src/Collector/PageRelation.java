import java.io.Serializable;

public class PageRelation implements Serializable {
    private int page; // numero de page
    private float tf; // TF normalise

    public PageRelation(int page, float tf) {
        this.page = page;
        this.tf = tf;
    }

    public float getTF() {
        return tf;
    }
}
