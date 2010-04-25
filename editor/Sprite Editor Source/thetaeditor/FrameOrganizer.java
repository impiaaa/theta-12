/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package thetaeditor;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.image.BufferedImage;
import javax.imageio.*;
import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.dnd.*;
import java.awt.datatransfer.*;

/**
 *
 * @author garrett
 */
public class FrameOrganizer extends JButton implements Scrollable {
    private LinkedList<Frame> frames = new LinkedList<Frame>();

    private Hashtable<Integer, Boolean> selected = new Hashtable<Integer, Boolean>();

    private volatile Point mouse = new Point(-1, -1);
    private volatile Point dragStart = null;
    private volatile int lastIndexClicked = -1;
    private volatile int dragIndex = -1;
    private volatile boolean dragging = false;

    private boolean flipX = false;
    private boolean flipY = false;

    private int idealWidth = 0;
    private int idealHeight = 0;


    public static void main(String[] args) {
        SequenceFrame.main(args);
    }

    public FrameOrganizer() {
        setPreferredSize(new Dimension(476, 167));

        Listener l = new Listener();
        addMouseListener(l);
        addMouseMotionListener(l);

        KeyEars ke = new KeyEars();
        addKeyListener(ke);

        Updater u = new Updater();
        u.start();

        Dropper dropper = new Dropper();
        DropTarget dt = new DropTarget(this, DnDConstants.ACTION_COPY_OR_MOVE,
        dropper, true, null);
        this.setDropTarget(dt);

//        // debug
//        for (int i = 0; i < 50; i++) {
//            addImage("/home/garrett/Pictures/ablogo.png");
//            frames.set(i, new Frame("/home/garrett/Pictures/ablogo.png"));
//        }
//        System.out.println("Thumbs: " + frames.size());

        setFocusable(true);
    }

    
    public void setFlipX(boolean b) {
        this.flipX = b;
    }
    public void setFlipY(boolean b) {
        this.flipY = b;
    }

    // Scrollable methods
    public Dimension getPreferredScrollableViewportSize() {
        return new Dimension(475, 200);
    }

    public int getScrollableBlockIncrement(Rectangle visibleRect, int orientation, int direction) {
        if (orientation == SwingConstants.VERTICAL) {
            if (direction < 0) {
                int crow = (visibleRect.y-5)/55;
                int ty = 5 + (crow-1)*55;
                if (ty < 0) ty = 0;
                return visibleRect.y - ty;
            } else {
                int crow = (visibleRect.y+visibleRect.height-5)/55;
                int ty = 5 + (crow+1)*55;
                if (ty > idealHeight)
                    ty = idealHeight;
                return ty - (visibleRect.y + visibleRect.height);
            }
        } else {
            if (direction < 0) {
                int col = (visibleRect.x-5)/55;
                int tx = 5 + (col-1)*55;
                if (tx < 0) tx = 0;
                return visibleRect.x - tx;
            } else {
                int col = (visibleRect.x + visibleRect.width - 5)/55;
                int tx = 5 + (col+1)*55;
                if (tx > idealWidth)
                    tx = idealWidth;
                return tx - (visibleRect.x + visibleRect.width);
            }

        }
    }

    public boolean getScrollableTracksViewportHeight() {
        return false;
    }

    public boolean getScrollableTracksViewportWidth() {
        return true;
    }

    public int getScrollableUnitIncrement(Rectangle visibleRect, int orientation, int direction) {
        return getScrollableBlockIncrement(visibleRect, orientation, direction);
    }
    // end scrollable stuff



    public LinkedList<String> getFramePaths() {
        LinkedList<String> paths = new LinkedList<String>();
        for (Frame f : frames) {
            paths.add(f.path);
        }
        return paths;
    }

    public int numFrames() {
        return frames.size();
    }

    /** Testing purposes only */
    private BufferedImage genThumb(int num) {
        BufferedImage bi = new BufferedImage(
                50, 50, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = bi.createGraphics();
        FontMetrics fm = g.getFontMetrics();
        g.setColor(Color.BLACK);

        g.drawString(
                String.valueOf(num),
                25 - fm.stringWidth(String.valueOf(num))/2,
                40);

        g.dispose();
        return bi;
    }

    

    public BufferedImage getThumb(int num) {
        BufferedImage o = frames.get(num).thumb;
        int w = o.getWidth();
        int h = o.getHeight();

        int type = o.getType();
        if (type == 0)
            type = BufferedImage.TYPE_INT_ARGB;
        BufferedImage img = new BufferedImage(w, h, type);


        Graphics2D g = img.createGraphics();
        g.drawImage(o,
                flipX?w:0, flipY?h:0, flipX?-w:w, flipY?-h:h, null);
        g.dispose();
        return img;
    }


    private int rowLength() {
        return (getWidth()-5)/55;
    }

    private int getIndex(int gridX, int gridY) {
        return gridY * rowLength() + gridX;
    }

    private boolean inFrame(int x, int y) {
        int i = getIndexUngrid(x, y);
        Point p = getTopLeft(i);
        return x <= p.x + 50 && y <= p.y + 50;
    }

    private int getIndexUngrid(int x, int y) {
        x -= 5;
        x /= 55;
        y -= 5;
        y /= 55;
        return getIndex(x, y);
    }

    public ArrayList<Integer> intersects(Point start, Point end) {
        boolean dir = true;

        int indexA = getIndexUngrid(start.x, start.y);
        int indexB = getIndexUngrid(end.x, end.y);

        if (indexA > indexB) dir = false;

        int firstI = dir?indexA:indexB;
        int lastI = dir?indexB:indexA;


        ArrayList<Integer> ints = new ArrayList<Integer>();
        for (int i = firstI; i <= lastI; i++)
            ints.add(i);
        return ints;
    }

    /** Returns an array list of the selected frame indices. */
    public ArrayList<Integer> getSelected() {
        ArrayList<Integer> indices = new ArrayList<Integer>();

        // While it would be faster to enumerate through the keys
        // in the hash table, this method is superior because it
        // assures that the indices in order.
        for (int i = 0; i < frames.size(); i++) {
            if (isSelected(i)) {
                indices.add(i);
            }
        }

        return indices;
    }

    /** Is anything selected? */
    public boolean hasSelected() {
        Enumeration<Boolean> vals = selected.elements();
        while (vals.hasMoreElements()) {
            if (vals.nextElement())
                return true;
        }
        return false;
    }

    /** Is the frame at the index selected? */
    public boolean isSelected(int index) {
        Boolean b = selected.get(index);
        return b != null && b.booleanValue();
    }

    public void removeImages(int firstIndex, int lastIndex) {
        for (int i = firstIndex; i <= lastIndex; i++) {
            frames.remove(firstIndex); // No, this isn't a typo.
                                       // Each time we remove the first one,
                                       // All the others shift to the left.
        }
        updateDimensions();
    }

    /**
     * This assumes the indices are in order from least to greatest.
     * @param indices
     */
    public void removeImages(ArrayList<Integer> indices) {
        for (int i = indices.size()-1; i >= 0; i--) {
            removeImage(indices.get(i));
        }
    }

    public void removeImage(int i) {
        if (i < 0 || i >= frames.size()) return;
        frames.remove(i);
        updateDimensions();
    }

    public void insertImage(int i, String path) {
        if (i >= frames.size()) {
            addImage(path);
            return;
        }
        if (i <= 0) i = 0;
        try {
            frames.add(i, new Frame(path, ImageIO.read(new File(path))));
        } catch (Exception e) {
            System.err.println("Failed to read path! " + e);
            return;
        }
        updateDimensions();
    }

    public void addImage(File file) {
        try {
            frames.add(new Frame(file.getAbsolutePath(), ImageIO.read(file)));
        } catch (Exception e) {
            System.err.println("Failed to read path! " + e);
            return;
        }
        updateDimensions();
    }

    public void addImage(String path) {
        addImage(new File(path));
    }

    /**
     * updates the size of the component
     * when frames are added or removed.
     */
    private void updateDimensions() {


        int w = getWidth() - 5;
        int h = getHeight() - 5;

        if (w <= 50)
            return;

        w += 5;
        int rowLength = (getWidth()-5)/55;
        int rows = getRow(frames.size());
        if (frames.size() % rowLength != 0) {
            rows++;
        }
        h = Math.max(h, rows * 55) + 5;

        idealWidth = w;
        idealHeight = h;

        setPreferredSize(new Dimension(w, h));

        super.setVisible(false);
        super.setVisible(true);

        requestFocusInWindow();
    }

    private int getRow(int i) {
        return (55 * i) / (((getWidth()-5)/55) * 55);
    }

    private int getCol(int i) {
        return ((i*55) % (((getWidth()-5)/55)*55))/55;
    }

    private Point getTopLeft(int i) {
        return new Point(getCol(i)*55 + 5, getRow(i)*55 + 5);
    }
    private Point getCenter(int i) {
        return new Point(getCol(i)*55 + 30, getRow(i)*55 + 30);
    }

    private int beenPainted = 0;
    @Override
    public void paint(Graphics gg) {
        if (beenPainted == 0) {
            beenPainted = 1;
        } else if (beenPainted == 1) {
            beenPainted = 2;
            updateDimensions();
            return;
        }

        Graphics2D g = (Graphics2D)gg;
        g.setColor(Color.WHITE);
        g.fillRect(-1, -1, getWidth()+2, getHeight()+2);

        g.setColor(Color.BLACK);

        int w = getWidth() - 5;
        int h = getHeight() - 5;

        g.setFont(new Font("serif", Font.BOLD, 32));
        FontMetrics fm = g.getFontMetrics();
        
        Stroke k = g.getStroke();

        if (dragIndex != -1 && dragging) {
            g.setColor(Color.BLUE);
            Point p = getTopLeft(dragIndex);
            g.fillRect(p.x-3, p.y, 2, 50);
        }

        for (int i = 0; i < frames.size(); i++) {
            int row = getRow(i);
            int col = getCol(i);
            int x = col * 55 + 5;
            int y = row * 55 + 5;

            g.drawImage(getThumb(i), x, y, 50, 50, null);

            g.setColor(Color.BLACK);
            if (isSelected(i)) {
                g.setStroke(new BasicStroke(2));
                g.setColor(Color.RED);
            }
            g.drawRect(x, y, 50, 50);

            g.setStroke(k);
        }
    }


    private volatile boolean mouseDown = false;
    private void updateDrag() {
        if (mouseDown) {
            int i = getIndexUngrid(mouse.x, mouse.y);
            if (i > frames.size())
                i = frames.size();
            dragIndex = i;
        } else {
            dragIndex = -1;
        }
    }

    /**
     * Moves the frames at the given indices to the new location.
     * @param indices
     * @param toIndex
     * @return - the new indice of the first frame
     */
    private int move(ArrayList<Integer> indices, int toIndex) {
        int lessCount = 0;
        for (Integer i : indices)
            if (i < toIndex)
                lessCount++;

        toIndex -= lessCount;

        LinkedList<Frame> fs = new LinkedList<Frame>();
        for (int i = indices.size()-1; i >= 0; i--) {
            int f = indices.get(i);
            fs.add(frames.get(f));
            removeImage(f);
        }

        for (Frame f : fs)
            frames.add(toIndex, f);

        return toIndex;
    }

    private BufferedImage getThumb(BufferedImage in) {
        int ow = in.getWidth();
        int oh = in.getHeight();
        if (ow == 50 && oh== 50) return in;

        double factor = 1;
        if (ow > oh) { // Condition code will have to change
                        // if the thumbnail is not a square.
            factor = 50./ow;
        } else {
            factor = 50./oh;
        }

        int nw = (int)(factor * ow);
        int nh = (int)(factor * oh);

        BufferedImage out = new BufferedImage(50, 50, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = out.createGraphics();

        int x = 50/2 - nw/2;
        int y = 50/2 - nh/2;

        g.drawImage(in, x, y, nw, nh, null);

        
        g.dispose();
        return out;
    }

    class Frame {
        String path = "";
        BufferedImage thumb = null;
        public Frame() {}
        public Frame(String path) {
            this.path = path;
            if (path != null && path.length() > 0) {
                try {
                    thumb = getThumb(ImageIO.read(new File(path)));
                } catch (Exception e) {
                    
                }
            }
        }
        public Frame(BufferedImage thumb) {
            this.thumb = thumb;
        }
        public Frame(String path, BufferedImage thumb) {
            this.path = path;
            this.thumb = getThumb(thumb);
        }
    }

    class Updater extends Thread {
        @Override
        public void run() {
            while (true) {
                try {
                    Point frameP = getLocationOnScreen();
                    Point mS = MouseInfo.getPointerInfo().getLocation();
                    mouse.x = mS.x - frameP.x;
                    mouse.y = mS.y - frameP.y;

                    updateDrag();

                } catch (Exception e) {
                    // IllegalStateException, I think. Happens when
                    // frame isn't displayable yet.
                }

                repaint();

                try {
                    sleep(20);
                } catch (InterruptedException e) {

                }
            }
        }
    }

    private boolean isImagePath(String path) {
        path = path.trim().toLowerCase();
        int p = path.lastIndexOf('.');
        if (p == -1) return false;
        String ext = path.substring(p+1, path.length());
        String[] pos = "png,jpg,jpeg,gif".split(",");
        for (String s : pos)
            if (ext.equals(s))
                return true;
        return false;
    }

    private boolean validFile(String path) {
        File file = new File(path);
        if (!file.exists()) return false;
        return file.isDirectory() || isImagePath(file.getName());
    }
    private boolean validUrl(String path) {
        URL u = null;
        try {
            u = new URL(path);
        } catch (MalformedURLException e) {
            return false;
        }
        return true;
    }
    private boolean isUrl(String path) {
        if (!path.matches("[a-zA-Z]+://")) return false;
        return validUrl(path);
    }


    class Dropper implements DropTargetListener {

        public void dragEnter(DropTargetDragEvent dtde) {

        }

        public void dragExit(DropTargetEvent dte) {

        }

        public void dragOver(DropTargetDragEvent dtde) {

        }

        public void drop(DropTargetDropEvent dtde) {
            dtde.acceptDrop(dtde.getDropAction());
            Transferable trans = dtde.getTransferable();

            Point p = dtde.getLocation();

            int index = getIndexUngrid(p.x, p.y);

            if (trans.isDataFlavorSupported(DataFlavor.stringFlavor)) {
                try {
                    String path = (String) trans
                            .getTransferData(DataFlavor.stringFlavor);
                    path = path.trim();
                    
                    boolean hasNewline = false;
                    for (int i = 0; i < path.length(); i++) {
                        char c = path.charAt(i);
                        if (c == '\n') {
                            hasNewline = true;
                            break;
                        }
                    }
                    if (hasNewline) {
                        System.out.println("Importing multiple files.");
                        String[] paths = path.split("\n");
                        for (int i = paths.length-1; i >= 0; i--) {
                            String s = paths[i];
                            s = s.trim();
                            if (s.length() > 0)
                                importString(index, s);
                        }
                    } else {
                        importString(index, path);
                    }
                } catch (Exception e) {
                    System.err.println("Oops! " + e);
                }
            }
        }

        public void dropActionChanged(DropTargetDragEvent dtde) {

        }

        private void importString(int index, String path) {
            if (index >= frames.size()) index = 0;

            if (path.toLowerCase().matches("file://.*")) {
                path = path.substring("file://".length()); // so there
                path = path.replaceAll("%20", " ");
            }

            System.out.println("Importing " + path);

            if (isUrl(path)) {
                System.out.println("URL MODE");
                URL u = null;
                try {
                    u = new URL(path);
                } catch (MalformedURLException e) {
                    // shouldn't happen, since we already
                    // checked in isUrl(path). But it might, if
                    // the connection cut out or something.
                    return;
                }
                BufferedImage img = null;
                try {
                    img = ImageIO.read(u);
                } catch (IOException e) {
                    return;
                }
                if (img != null) {
                    frames.add(index, new Frame(path, img));
                    System.out.println("Inserted at " + index);
                    return;
                }
            } else {
                System.out.println("File mode");
                File f = new File(path);
                if (!f.exists()) {
                    System.out.println("No such file (" + path + ")");
                    return;
                }
                if (f.isDirectory()) {
                    String[] sub = f.list();
                    for (String s : sub) {
                        if (isImagePath(s)) {
                            frames.add(index, new Frame(s));
                        }
                    }
                    return;
                } else if (isImagePath(f.getName())) {
                    frames.add(index, new Frame(f.getPath()));
                    System.out.println("Inserted at " + index);
                    return;
                } else {
                    System.out.println("No match: " + f.getPath());
                }
            }
        }
        
    }

    class Listener implements MouseListener, MouseMotionListener {
        private boolean lastWasGroup = false; // used for highlighting
        private ArrayList<Integer> lastHover = null;
        public void mouseClicked(MouseEvent e) {
            boolean inFrame = inFrame(e.getX(), e.getY());

            if (e.isShiftDown()) {
                if (lastIndexClicked != -1) {
                    ArrayList<Integer> hover = intersects(
                            getCenter(lastIndexClicked), mouse);

                    if (lastWasGroup && lastHover != null)
                        for (Integer i : lastHover)
                            selected.remove(i);
                        
                    for (Integer i : hover)
                        selected.put(i, true);

                    lastHover = hover;
                    lastWasGroup = true;
                } else {
                    lastWasGroup = false;
                }
            } else {
                lastWasGroup = false;

                if (inFrame) {
                    if (!e.isControlDown()) {
                        selected.clear();
                    }
                    int i = getIndexUngrid(e.getX(), e.getY());
                    if (e.isControlDown()) {
                        selected.put(i, !isSelected(i));
                    } else {
                        selected.put(i, true);
                    }
                    lastIndexClicked = getIndexUngrid(e.getX(), e.getY());
//                    System.out.println(lastIndexClicked);
                }
            }
        }

        public void mouseEntered(MouseEvent e) {

        }

        public void mouseExited(MouseEvent e) {

        }

        public void mousePressed(MouseEvent e) {
            if (inFrame(e.getX(), e.getY()) && !e.isControlDown() &&
                    !e.isShiftDown() &&
                    !isSelected(getIndexUngrid(e.getX(), e.getY()))) {
                    selected.clear();
                    selected.put(getIndexUngrid(e.getX(), e.getY()), true);
            }

            dragStart = e.getPoint();
            mouseDown = true;
        }

        public void mouseReleased(MouseEvent e) {
            if (hasSelected() && dragIndex != -1 && dragging) {
                ArrayList<Integer> sel = getSelected();
                int st = move(sel, dragIndex);
                selected.clear();
                
                for (int i = 0; i < sel.size(); i++) {
                    selected.put(st+i, true);
                }

                lastIndexClicked = st;
            }
            dragStart = null;
            mouseDown = false;
            dragging = false;
        }

        public void mouseMoved(MouseEvent e) {
            dragging = false;
        }

        public void mouseDragged(MouseEvent e) {
            dragging = true;
        }
    }

    class KeyEars implements KeyListener {


        public void keyPressed(KeyEvent e) {
            switch (e.getKeyCode()) {
                case KeyEvent.VK_DELETE:
                case KeyEvent.VK_BACK_SPACE:
                    removeImages(getSelected());
                    selected.clear();
                    break;
            }
        }
        public void keyReleased(KeyEvent e) {

        }
        public void keyTyped(KeyEvent e) {

        }
    }
}
