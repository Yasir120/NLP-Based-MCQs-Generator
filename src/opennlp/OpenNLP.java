/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package opennlp;

import static com.sun.org.apache.xerces.internal.util.DOMUtil.setVisible;
import java.awt.FlowLayout;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JFrame;
import static javax.swing.JFrame.EXIT_ON_CLOSE;
import javax.swing.JLabel;
import javax.swing.JTextField;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSSample;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.tokenize.SimpleTokenizer;

public class OpenNLP extends JFrame {
public OpenNLP( int textboxsize, int labelsize,int btnsize) {
        setSize(600, 480);
        setVisible(true);
        setLayout(new FlowLayout());
        setTitle("NLP based GUI");
        setLocationRelativeTo(null);
        setAlwaysOnTop(true);
        setResizable(false);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        //mybtn=new JButton("Button");
        //add(mybtn);
        JLabel[] label = new JLabel[labelsize];
        for (int i = 0; i < label.length; i++) {
            label[i] = new JLabel("label" + i);
            add(label[i]);
            show();
        }
        JTextField[] textbox = new JTextField[textboxsize];
        for (int i = 0; i < textbox.length; i++) {
            textbox[i] = new JTextField(10);
            add(textbox[i]);
            show();
        }
        JButton[] btn = new JButton[btnsize];
        for (int i = 0; i < btn.length; i++) {
            btn[i] = new JButton("Button " + i);
            add(btn[i]);
            show();
        }
    }
    public static void main(String[] args) throws FileNotFoundException, IOException {
        ArrayList<String> postags = new ArrayList<>();
        ArrayList<String> textfields = new ArrayList<>();
        ArrayList<String> buttons = new ArrayList<>();
        ArrayList<String> labels = new ArrayList<>();
        String Text1 = "";
        //  String sentence = "Create GUI for Book List Management having following fields Id ,name ,author ,publisher. Apply Collection Framework on it and perform insertion and searching using ArrayList searching concepts.";
        //String sentence="Create GUI system for students which asks 5 questions to allowed students. Every question has four options in which one option is correct. The system compares a student’s result with another student’s result. The student who tops among the students comes at first position and so on. There should be a login form for student authentication. The system asks five questions from questions pool to the student. The student’s answer to the question should be saved in the database. At the end of the test, the result of questions should be shown. At the end of the test, the student should be able to see position among the other students.";
        String sentence = "  A user shall be able to enter information on an incident, including, location, description and time period. A user shall be able to enter cnic or close the frame with close button.";
       // String sentence="A user shall be able to enter cnic or close the frame with close button.";
        String[] CS = sentence.split(",");
        for (int i = 0; i < CS.length; i++) {
            //System.out.print(CS[i]);
            Text1 = Text1 + CS[i];
        }
        System.out.println(Text1);
        System.out.println("");
        //Loading sentence detector model 
        InputStream inputmodel = new FileInputStream("C:/OpenNLP_models/en-sent.bin");
        SentenceModel model = new SentenceModel(inputmodel);

        //Loading Parts of speech-maxent model       
        InputStream inputStream = new FileInputStream("C:/OpenNLP_models/en-pos-maxent.bin");
        POSModel model1 = new POSModel(inputStream);

        //Instantiating the SentenceDetectorME ,this class contains methods to split the raw text into sentences
        SentenceDetectorME detector = new SentenceDetectorME(model);

        //Detecting the sentence
        String sentences[] = detector.sentDetect(Text1);

        //Printing the sentences 
        for (String sent : sentences) {
            System.out.println(sent);
            //Instantiating POSTaggerME class 
            POSTaggerME tagger = new POSTaggerME(model1);

            //Instantiating SimpleTokenizer class 
            //In both the classes, there are no constructors available to instantiate them. 
            //Therefore, we need to create objects of these classes using the static variable INSTANCE.
            SimpleTokenizer tokenizer = SimpleTokenizer.INSTANCE;
            //Tokenizing the given sentence 
            String tokens[] = tokenizer.tokenize(sent);

            //Generating tags 
            String[] tags = tagger.tag(tokens);
            POSSample sample = new POSSample(tokens, tags);
            String[] mytoken = sample.getSentence();
            for (int i = 0; i < mytoken.length; i++) {
                System.out.println(tokens[i] + "=" + tags[i]);
                postags.add(tags[i]); 
            }
            for (int i = 0; i < tags.length; i++) {
                if (tags[i].equals("VBG") && tags[i - 1].equals("NN")) {
                    if (tags[i + 1].equals("NN")) {
                        textfields.add(tags[i + 1]);
                        labels.add(tags[i + 1]);
                    }
                    if (tags[i + 2].equals("NN")) {
                        textfields.add(tags[i + 2]);
                        labels.add(tags[i + 2]);
                    }
                }
                if(tags[i].equals("CC"))
                {
                    if (tags[i + 1].equals("NN")) {
                        textfields.add(tags[i + 1]);
                        labels.add(tags[i + 1]);
                    }
                   
                }
                if(tags[i].equals("VB")&& tags[i - 1].equals("TO"))
                {
                    if (tags[i + 1].equals("JJ")) {
                        textfields.add(tags[i + 1]);
                        labels.add(tags[i + 1]);
                    }
                }
                 if(tags[i].equals("JJ"))
                {
                    if (tags[i + 1].equals("NN")) {
                        buttons.add(tags[i + 1]);
                    }
                }
            }
        }
        System.out.println("");
        OpenNLP obj=new OpenNLP(textfields.size(),labels.size(),buttons.size());
        
        
    }
}
