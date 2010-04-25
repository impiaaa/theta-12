/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package thetaeditor;
import java.io.*;
import java.util.*;

/**
 *
 * @author garrett
 */
public class Exporter {
    private String name;
    private ArrayList<Sprite> sprites = new ArrayList<Sprite>();
    private Hashtable<String, String> moving = new Hashtable<String, String>();
    private Statusable stat;

    
    public Exporter(Statusable stat, ArrayList<Sprite> sprites, String name) {
        if (!name.toLowerCase().endsWith(".xml"))
            name += ".xml";

        this.name = name;
        this.sprites = sprites;
        this.stat = stat;
    }

    public void export(String targetDir) {
        File dir = new File(targetDir);
        if (!dir.exists()) {
            if (!dir.mkdirs()) {
                stat.setStatus("Failed to create export dir.");
            }
        }
        stat.setStatus("Indexing files...");
        assembleFiles(targetDir);
        stat.setStatus("Relativizing paths...");
        relativizePaths(targetDir);
        stat.setStatus("Copying frames...");
        copyFiles();
        stat.setStatus("Saving " + name + "...");
        saveXML(targetDir);
    }

    private void saveXML(String targetDir) {
        stat.setStatus("Generating xml...");
        String text = storeXML();
        File xf = new File(targetDir + File.separator + name);
        stat.setStatus("Writing xml...");
        PrintWriter out = null;
        try {
            out = new PrintWriter(xf);
            out.println(text);
            out.close();
            stat.setStatus("XML Saved.");
        } catch (IOException e) {
            stat.setStatus("Error writing xml!");
        }
    }

    private String storeXML() {
        StringBuffer sb = new StringBuffer(1000);
        sb.append("<spritelist relative=\"1\">\n");
        for (Sprite s : sprites) {
            sb.append("\t");
            sb.append(s.store().trim().replaceAll("\n", "\n\t"));
            sb.append("\n");
        }
        sb.append("</spritelist>");
        return sb.toString();
    }

    private void copyFiles() {
        int file = 0;
        int files = moving.size();
        int failed = 0;
        Enumeration<String> froms = moving.keys();
        while (froms.hasMoreElements()) {
            file++;
            int per = (int)(100. * file / files);
            stat.setStatus("Copying " + file + "/" + files + " (%" + per
                    + "), " + failed + " failed.");

            String from = froms.nextElement();
            String to = moving.get(from);
            if (!copy(from, to)) failed++;
        }
    }

    private void relativizePaths(String tarDir) {
        for (Sprite sprite : sprites) {
            Enumeration<String> keys = sprite.sequences.keys();
            while (keys.hasMoreElements()) {
                String key = keys.nextElement();
                Sequence sequence = sprite.sequences.get(key);
                for (int i = 0; i < sequence.frames.size(); i++) {
                    String o = sequence.frames.get(i);
                    String absN = moving.get(o);
                    String relN = absN.substring(tarDir.length()+1);
                    sequence.frames.set(i, relN);
                }
            }
        }
    }

    private void assembleFiles(String tarDir) {
        Hashtable<String, String> used =
                new Hashtable<String, String>();

        System.out.println("Name: " + name);
        int dot = name.lastIndexOf('.');
        String subname = name.substring(0, dot);
        System.out.println("Subname: " + subname);

        for (Sprite sprite : sprites) {
            Enumeration<String> keys = sprite.sequences.keys();
            while (keys.hasMoreElements()) {
                String key = keys.nextElement();
                Sequence sequence = sprite.sequences.get(key);
                for (String path : sequence.frames) {
                    File file = new File(path);
                    if (!file.exists() || file.isDirectory()) continue;
                    String s = file.getAbsolutePath();
                    String[] parts = getParts(s);
                    String tar = null;
                    int ntry = 0;
                    do {
                        tar = tarDir + File.separator + subname +
                            File.separator + "sprites"
                            + File.separator + parts[1] +
                            (ntry==0?"":ntry) + parts[2];
                        
                        ntry++;
                    } while (used.containsKey(tar) &&
                            !used.get(tar).equals(s));
                    
                    used.put(tar, s);
                    moving.put(s, tar);
                }
            }
        }
    }

    private void moveImages(Sequence seq, String targetDir) {
        for (int i = 0; i < seq.frames.size(); i++) {
            String opath = seq.frames.get(i);
            String[] parts = getParts(opath);
            if (parts[0].equals(targetDir))
                continue; // Already in correct directory.

            int ap = 0;
            String newpath = null;
            do {
                newpath = targetDir + File.separator + parts[1] +
                        (ap==0?"":("_"+ap)) + parts[2];
                ap++;
            } while (new File(newpath).exists());
            if (!copy(opath, newpath)) {
                System.err.println("Failed to copy \"" + opath + "\" to \"" +
                        newpath + "\"!");
                continue;
            }
            seq.frames.set(i, newpath);
        }
    }

    /**
     * Picks apart the path into an array.<br>
     * Input <b>/home/user/foo.png</b><br>
     * Output <b>{"/home/usr", "foo", ".png"}</b>
     * @param path
     * @return a String[] of the parts.
     */
    private String[] getParts(String path) {
        int fsep = path.lastIndexOf(File.separator);
        if (fsep == -1)
            return new String[] {".", path};
        String[] parts = new String[] {
            path.substring(0, fsep),
            path.substring(fsep+1, path.length()),
            ""
        };
        int esep = parts[1].lastIndexOf('.');
        if (esep == -1) {
            return parts;
        }
        parts[2] = parts[1].substring(esep, parts[1].length());
        parts[1] = parts[1].substring(0, esep);
        return parts;
    }

    private boolean copy(String path1, String path2) {
        if (path1.equals(path2)) return true; // No need, obviously.

        File file1 = new File(path1);
        File file2 = new File(path2);
        if (!file1.exists()) return false;

        if (!file2.getParentFile().exists())
            if (!file2.getParentFile().mkdirs())
                return false;

        InputStream in = null;
        try {
            in = new FileInputStream(file1);
        } catch (IOException e) {
            System.err.println("Error initializing input stream: " + e);
            return false;
        }
        OutputStream out = null;
        try {
            out = new FileOutputStream(file2);
        } catch (IOException e) {
            System.err.println("Error initializing output stream: " + e);
        }

        byte[] buf = new byte[512];
        int read = 0;
        try {
            while ((read = in.read(buf)) != 0) {
                if (read <= 0) break; // We're done.
                out.write(buf, 0, read);
            }
        } catch (IOException e) {
            
        }
        try {
            in.close();
            out.close();
            return true;
        } catch (IOException e) {
            System.err.println("Error closing stream(s): " + e);
            return false;
        }
    }

    private void rm(File file) {
        if (!file.isDirectory()) file.delete();
        File[] ls = file.listFiles();
        for (File f : ls) {
            rm(f);
        }
    }
}
