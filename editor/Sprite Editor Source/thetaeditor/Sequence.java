/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package thetaeditor;

import java.util.LinkedList;
import java.io.*;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;

/**
 *
 * @author garrett
 */
public class Sequence {

    LinkedList<String> frames = new LinkedList<String>();
    double duration = 1;
    boolean flipX = false;
    boolean flipY = false;
    boolean loop = false;
    String name = null;

    public String store() {
        return store(null);
    }

    public String store(String name) {
        if (name == null && this.name != null) {
            name = this.name;
        }

        StringBuffer sb = new StringBuffer(1000);
        sb.append("<sequence duration=\"");
        sb.append(duration);
        if (name != null && name.trim().length() > 0) {
            sb.append("\" name=\"");
            sb.append(name.trim());
        }
        sb.append("\" flipx=\"");
        sb.append(flipX ? 1 : 0);
        sb.append("\" flipy=\"");
        sb.append(flipY ? 1 : 0);
        sb.append("\" loop=\"");
        sb.append(loop ? 1 : 0);
        sb.append("\">\n");
        for (String s : frames) {
            sb.append("\t<frame>");
            sb.append(s);
            sb.append("</frame>\n");
        }
        sb.append("</sequence>\n");
        return sb.toString();
    }

    @Override
    public String toString() {
        return store();
    }

    public void read(String data) {
        Sequence.read(this, data);
    }

    public static Sequence read(Sequence seq, Node node) {
        return Sequence.read("", seq, node);
    }
    public static Sequence read(String base, Sequence seq, Node node) {
        try {
            NamedNodeMap atts = node.getAttributes();
            seq.duration = Double.parseDouble(
                    atts.getNamedItem("duration").getNodeValue());
            seq.flipX = atts.getNamedItem("flipx").getNodeValue().equals("1");
            seq.flipY = atts.getNamedItem("flipy").getNodeValue().equals("1");
            seq.loop = atts.getNamedItem("loop").getNodeValue().equals("1");

            Node nameNode = atts.getNamedItem("name");
            if (nameNode != null) {
                seq.name = nameNode.getNodeValue();
            }

            seq.frames.clear();

            NodeList nodes = node.getChildNodes();
            for (int i = 0; i < nodes.getLength(); i++) {
                Node n = nodes.item(i);
                String path = n.getTextContent().trim();
                if (path.length() > 0) {
                    seq.frames.add((base.length()>0?(base + File.separator):"") + path);
                }
            }
        } catch (Exception e) {
        }
        return seq;
    }

    public static Sequence read(Sequence seq, String data) {
        return Sequence.read("", seq, data);
    }
    /** Reads the xml data into the sequence */
    public static Sequence read(String base, Sequence seq, String data) {
        if (seq == null) seq = new Sequence();
        try {
            DocumentBuilderFactory factory =
                    DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Reader reader = new CharArrayReader(data.toCharArray());
            Document doc = builder.parse(new org.xml.sax.InputSource(reader));

            TransformerFactory tranFact = TransformerFactory.newInstance();
            Node node = doc.getDocumentElement();

            Sequence.read(base, seq, node);
        } catch (Exception e) {
            System.err.println("XML Error: " + e);
            return null;
        }

        return seq;
    }

    public static void main(String[] args) throws Exception {
        Sequence seq = new Sequence();
        seq.duration = 5;
        seq.flipX = false;
        seq.flipY = false;
        seq.loop = true;

        for (int i = 0; i < 3; i++) {
            seq.frames.add("Frame " + i);
        }
        seq.read(seq.store());
        System.out.println("Store: \n" + seq.store());
    }
}
