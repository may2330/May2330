import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.*;

public class Test2 { //jw
	
	public static void main(String[] args) {
		int life_counter = 10;
		ImageIcon back = new ImageIcon("back.jpg");
		ImageIcon heart = new ImageIcon("heart.jpg");
		ImageIcon heart2 = new ImageIcon("heart2.jpg");
		ImageIcon send = new ImageIcon("send.jpg");
		JFrame cp = new JFrame("The card game");
		JPanel text_input = new JPanel();
		JPanel card_panel = new JPanel();
		JPanel chat_panel = new JPanel();
		JLabel timer = new JLabel("30 seconds");
		JTextArea problem = new JTextArea();
		JPanel Problem_panel = new JPanel();
		JTextField input_line = new JTextField("type here",10);
		JTextArea MessageArea = new JTextArea("Chatting Message here");
		JScrollPane Message_pane = new JScrollPane();
		JPanel life_panel = new JPanel();
		JLabel life_arr[] = new JLabel[10];
		boolean life_state[] = {true,true,true,true,true,true,true,true,true,true};
		
		card_panel.setLayout(null);
		card_panel.setBounds(50, 450, 1060, 250);
		card_panel.setBackground(new Color(136,133,164));
		
		JButton button1 = new JButton(back);
		JButton button2 = new JButton(back);
		JButton button3 = new JButton(back);
		JButton button4 = new JButton(back);
		JButton button5 = new JButton(back);
		card_panel.add(button1);
		card_panel.add(button2);
		card_panel.add(button3);
		card_panel.add(button4);
		card_panel.add(button5);
		button1.setBounds(10,10,200,230);
		button2.setBounds(220,10,200,230);
		button3.setBounds(430,10,200,230);
		button4.setBounds(640,10,200,230);
		button5.setBounds(850,10,200,230);
		
		button1.addMouseListener(new MouseListener(){


			public void mouseClicked(MouseEvent e) {}

			public void mouseEntered(MouseEvent e) {
				button1.setBorder(BorderFactory.createLineBorder(Color.RED, 3));
			}

			public void mouseExited(MouseEvent e) {button1.setBorder(null);}

			public void mousePressed(MouseEvent e) {
				//button1.setBorder(BorderFactory.createLineBorder(Color.RED, 3));
			}

			public void mouseReleased(MouseEvent e) {
				//button1.setBorder(null);		
			}	
		});
		
		life_panel.setLayout(null);
		setlife(life_panel,life_arr,heart);
		life_panel.setBounds(1150, 600, 200, 68);
		life_panel.setBackground(new Color(245,209,183));
		
		JButton send_button = new JButton(send);
		send_button.setBounds(265,5,80,30);
		text_input.add(send_button);

		input_line.setEditable(true);
		input_line.setBounds(10,5,250,30);
		text_input.add(input_line);
		text_input.setLayout(null);
		text_input.setBounds(10, 280, 350, 40);
		text_input.setBackground(new Color(136,133,150));
		
		MessageArea.setBackground(new Color(136,133,150));
		MessageArea.setEditable(false);
		MessageArea.setLayout(null);
		MessageArea.setBounds(0, 0, 350, 260);
		MessageArea.setLineWrap(true);
		
		Message_pane.setBounds(10,10,350,260);
		Message_pane.setViewportView(MessageArea);
		Message_pane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		Message_pane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		
		chat_panel.setLayout(null);
		chat_panel.setBounds(1100, 50, 370, 345);
		chat_panel.setBorder(BorderFactory.createSoftBevelBorder(0));
		chat_panel.add(text_input);
		chat_panel.add(Message_pane);
		
		timer.setBounds(900,15,100,30);
		timer.setBorder(BorderFactory.createBevelBorder(1));
		timer.setForeground(Color.red);
		timer.setFont(new Font(Font.DIALOG, Font.ITALIC, 14));
		
		problem.setBounds(10,60,1000,300);
		problem.setBorder(null);

		Problem_panel.setLayout(null);
		Problem_panel.setBounds(50,50,1020,380);
		Problem_panel.setBackground(new Color(122,154,130));
		Problem_panel.add(timer);
		Problem_panel.add(problem);
		
		cp.setLayout(null);
		cp.setBounds(250,150,1500,800);
		cp.add(life_panel);
		cp.add(card_panel);
		cp.add(chat_panel);
		cp.add(Problem_panel);
		cp.setVisible(true);
		cp.setResizable(false);
	
	cp.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	public static void setlife(JPanel life_panel,JLabel life_arr[],ImageIcon heart) // initial setting
	{
		int i;
		int width = 40 , height = 34;
		
		for(i=0; i<10; i++)
		{
			life_arr[i] = new JLabel();
			life_arr[i].setIcon(heart);
			life_arr[i].setBounds((i%5)*width,(i/5)*height,width,height);
			life_panel.add(life_arr[i]);
		}
	}
	
	public static void update_life(boolean life_state[],JLabel life_arr[],ImageIcon heart2,int counter) // ActionListener call this method to update current life.
	{		
		int i;
		int width = 40 , height = 34;
		
		for(i=counter; i<10; i++)
		{
			if(life_state[i] == true)
				life_state[i] = false;
			life_arr[i].setIcon(heart2);
			life_arr[i].setBounds((i%5)*width,(i/5)*height,width,height);
		}
	}
}