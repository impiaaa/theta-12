/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package thetaeditor;
import java.util.Hashtable;
import java.util.Enumeration;
import java.io.*;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;

/**
 *
 * @author garrett
 */
public class Sprite {

    Hashtable<String, Sequence> sequences = new Hashtable<String, Sequence>();
    String defaultSequence = "";
    String name = "Untitled Sprite";

    /**
     * Testing purposes only.
     * @param args
     */
    public static void main(String[] args) {
        Sprite sp = new Sprite();
        sp.name = "Foo";
        sp.defaultSequence = "Bar";
        Sequence seq = new Sequence();
        seq.flipX = true;
        seq.flipY = false;
        seq.loop = true;
        seq.duration = 5.4;
        seq.frames.add("test frame 1");
        seq.frames.add("test frame 2");
        sp.sequences.put("Bar", seq);
        Sequence seq2 = new Sequence();
        seq2.flipX = false;
        seq2.flipY = true;
        seq2.loop = false;
        seq2.duration = 17.8;
        seq2.frames.add("test frame 1a");
        seq2.frames.add("test frame 2b");
        sp.sequences.put("Banana", seq2);

        String store = sp.store();
        sp = Sprite.read(sp, store);
        System.out.println(sp.store());
    }

    @Override
    public String toString() {
        return name + " (" + sequences.size() + " sequences)";
    }

    private String sanitize(String input) {
        return input.replaceAll("[\"'<>\\{\\}\\[\\]\\(\\)]+", "");
    }

    public void read(String data) {
        Sprite.read(this, data);
    }

    public String store() {
        StringBuffer sb = new StringBuffer(1000 * sequences.size());

        sb.append("\n<sprite name=\"");
        sb.append(sanitize(name));
        sb.append("\" default=\"");
        sb.append(sanitize(defaultSequence));
        sb.append("\">\n");

        Enumeration<String> keys = sequences.keys();
        while (keys.hasMoreElements()) {
            String key = keys.nextElement();
            Sequence seq = sequences.get(key);
            String store = seq.store(key).trim();
            store = store.replaceAll("\n", "\n\t");
            sb.append("\t");
            sb.append(store);
            sb.append("\n");
        }
        sb.append("</sprite>\n");

        return sb.toString();
    }

    public static Sprite read(Sprite sprite, String data) {
        try {
            DocumentBuilderFactory factory =
                    DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Reader reader = new CharArrayReader(data.toCharArray());
            Document doc = builder.parse(new org.xml.sax.InputSource(reader));
            Node node = doc.getDocumentElement();
            return Sprite.read(sprite, node);
        } catch (Exception e) {
            System.err.println("Error parsing sprite: " + e);
        }
        return sprite;
    }

    public static Sprite read(Sprite sprite, Node node) {
        return Sprite.read("", sprite, node);
    }
    public static Sprite read(String base, Sprite sprite, Node node) {
        if (sprite == null) sprite = new Sprite();
        try {

            NamedNodeMap atts = node.getAttributes();
            sprite.name = atts.getNamedItem("name").getNodeValue();
            sprite.defaultSequence = atts.getNamedItem("default").getNodeValue();

            NodeList children = node.getChildNodes();
            for (int i = 0; i < children.getLength(); i++) {
                Node n = children.item(i);
                if (n == null) continue;
                NamedNodeMap catts = n.getAttributes();
                if (catts == null) continue;
                Node cnameNode = catts.getNamedItem("name");
                if (cnameNode == null) continue;
                String cname = cnameNode.getNodeValue();
                sprite.sequences.put(cname, Sequence.read(base, new Sequence(), n));
            }
        } catch (Exception e) {
            System.err.println("Error parsing sprite: " + e);
        }
        return sprite;
    }

    @Override
    public Sprite clone() {
        return Sprite.read(new Sprite(), store());
    }
}
