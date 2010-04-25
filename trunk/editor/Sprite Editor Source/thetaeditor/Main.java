/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package thetaeditor;
import javax.swing.*;

/**
 *
 * @author garrett
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            // Set cross-platform Java L&F (also called "Metal")
            UIManager.setLookAndFeel(
                    UIManager.getSystemLookAndFeelClassName());
        } catch (UnsupportedLookAndFeelException e) {
            // handle exception
        } catch (ClassNotFoundException e) {
            // handle exception
        } catch (InstantiationException e) {
            // handle exception
        } catch (IllegalAccessException e) {
            // handle exception
        }


        new Main();
    }

    public Main() {
        SpriteLibraryFrame lib = new SpriteLibraryFrame();
        lib.setVisible(true);
    }
}
