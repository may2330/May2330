import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.util.ArrayList;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Exchange extends JFrame{ //전체 프레임에서 내 deck info랑 새로운 또는 상대방 deck info를 받아서 실제 Deck클래스에 insert해서 이미지를 변경해준다.

	private static final int card_max = 5;
	private JLabel my_list;
	private JLabel new_list;
	private Deck my_deck;
	private Deck new_deck;
	private JButton get;
	private ImageIcon get_img;
	private JButton drop;
	private ImageIcon drop_img;
	private ImageIcon background_img;
	private int type;  // 0 = new_deck , 1 = my_deck
	public int send_result=0;
	
	MouseListener add_handler = new MouseListener()
	{

		public void mouseClicked(MouseEvent e) {
			add_event();
		}
		public void mouseEntered(MouseEvent e) {
			
		}
		public void mouseExited(MouseEvent e) {}
		public void mousePressed(MouseEvent e) {}
		public void mouseReleased(MouseEvent e) {}
	};
	
	MouseListener drop_handler = new MouseListener()
	{

		public void mouseClicked(MouseEvent e) {
			drop_event();
		}
		public void mouseEntered(MouseEvent e) {
			
		}
		public void mouseExited(MouseEvent e) {}
		public void mousePressed(MouseEvent e) {}
		public void mouseReleased(MouseEvent e) {}
	};
	
	public Exchange(Deck original)
	{
		this.setName("Shift card");
		this.setLayout(null);
		this.setBounds(50, 100, 1150, 860);
		this.getContentPane().setBackground(new Color(244,101,40));
		this.setDefaultCloseOperation(HIDE_ON_CLOSE);
		this.addWindowListener(new WindowListener(){
			public void windowActivated(WindowEvent arg0) {}
			public void windowClosed(WindowEvent arg0) {				
			}
			public void windowClosing(WindowEvent arg0) { // x 버튼 누르면서 default close인 hide되는데 그 때 메인 게임창에 업데이트를 해준다.
				original.set_info(my_deck.get_info());
				original.reset();
				if(send_result==1)
					original.addEvent(3);
				//System.out.println("Closed!!");
			}
			public void windowDeactivated(WindowEvent arg0) {}
			public void windowDeiconified(WindowEvent arg0) {}
			public void windowIconified(WindowEvent arg0) {}
			public void windowOpened(WindowEvent arg0) {}			
		});
		new_deck = new Deck(); // 0으로 초기화 되있음 생성하면
		new_deck.setBounds(50,80,1060,250);
		add(new_deck);
		
		my_deck = new Deck();
		my_deck.reset();
		my_deck.setBounds(50,450,1060,250);
		add(my_deck);
		
		my_list = new JLabel("Your Deck ");
		my_list.setBounds(50,400,100,10);
		add(my_list);
		
		new_list = new JLabel("New Deck ");
		new_list.setBounds(50,30,100,10);
		add(new_list);

		get = new JButton();
		get_img = new ImageIcon("get.png");
		get.setIcon(get_img);
		get.setBounds(330,730,103,58);
		get.addMouseListener(add_handler);
		add(get);
		
		drop = new JButton();
		drop_img = new ImageIcon("drop.jpg");
		drop.setIcon(drop_img);
		drop.setBounds(720,730,103,58);
		drop.addMouseListener(drop_handler);
		add(drop);	
	}
	
	public void my_deck_set_info(ArrayList<Integer> temp)
	{
		my_deck.set_info(temp);
		my_deck.reset();
	}
	public void new_deck_set_info(ArrayList<Integer> temp)
	{
		new_deck.set_info(temp);
		new_deck.reset();
	}
	public void add_event()
	{
		int event_button = this.getBtn();
		if(type == 0)
			my_deck.Insert(new_deck.send(event_button));
	}
	public void drop_event()
	{
		int event_button = this.getBtn();
		if(type == 0)
			new_deck.Delete(event_button);
		else
			my_deck.Delete(event_button);
	}
	public int getBtn()
	{
		if(my_deck.get_pressed_time() > new_deck.get_pressed_time())
		{
			type = 1;
			return my_deck.get_pressed_button();
		}
		else
		{
			type = 0;
			return new_deck.get_pressed_button();
		}		
	}
	public void openSet()  // 추가됨!!
	{
		my_deck.addEvent(1);
		new_deck.addEvent(1);
	}
}


