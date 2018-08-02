import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.net.URL;
import java.util.ArrayList;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.swing.*;

public class Test extends JPanel{ //jw


	private int life_counter;
	private int time;

	//private ImageIcon back;
	private ImageIcon heart;
	private ImageIcon heart2;
	private ImageIcon send;
	private ImageIcon lock;
	private ImageIcon temp;
	private ImageIcon one;
	private ImageIcon two;
	private ImageIcon three;
	private ImageIcon four;
	private ImageIcon logo_start,logo_turn,logo_attack,logo_correct,logo_wrong,logo_win,logo_lose;

	private static JPanel Problem_panel;
	private static JPanel chat_panel;
	private JPanel text_btn_panel;
	private static Deck card_panel;
	private static JPanel life_panel;
	private static JPanel total_life;

	private Font font;
	private JLabel timer;
	private JLabel life_name_1;
	private JLabel life_name_2;
	private JLabel life_name_3;
	private JLabel life_name_4;
	private JLabel life_heart_1;
	private JLabel life_heart_2;
	private JLabel life_heart_3;
	private JLabel life_heart_4;
	private JLabel life_1_num;
	private JLabel life_2_num;
	private JLabel life_3_num;
	private JLabel life_4_num;
	private JLabel problem;

	private JTextField input_line;
	private JTextArea MessageArea;
	private JScrollPane Message_pane;
	
	private ArrayList<Integer> card_info;
	private ArrayList<Integer> new_card_info;
	private Exchange card_exchange;
	private ArrayList<JButton> answers;
	
	private JLabel life_arr[] = new JLabel[10];
	boolean life_state[] = {true,true,true,true,true,true,true,true,true,true};
	
	private URL url;
	private Clip clip;
	private Clip temp_clip;
	
	private boolean state[] = new boolean[7];
	private Image logo[] = new Image[7];
	private URL urls[] = new URL[6];

	static int timer_set = 30;
	static int who_timer_set = 30;
	private static int attacked = 0;
	private int i;
	
	private MouseListener answer_button_listener;
	
	public Test(Client client)
	{
		heart = new ImageIcon("heart.jpg");
		heart2 = new ImageIcon("heart2.png");
		send = new ImageIcon("send.jpg");
		lock = new ImageIcon("lock.png");
		temp = new ImageIcon("back2.jpg");
		one = new ImageIcon("one.png");
		two = new ImageIcon("two.png");
		three = new ImageIcon("three.png");
		four = new ImageIcon("four.png");
		
		logo_start = new ImageIcon("start.png");
		logo_turn = new ImageIcon("turn.jpg");
		logo_attack = new ImageIcon("attack.jpg");
		logo_correct = new ImageIcon("correct.jpg");
		logo_wrong = new ImageIcon("wrong.jpg");
		logo_win = new ImageIcon("win.jpg");
		logo_lose = new ImageIcon("lose.png");

		Problem_panel = new JPanel();
		chat_panel = new JPanel();
		text_btn_panel = new JPanel();
		card_panel = new Deck();
		life_panel = new JPanel();
	    
		font = new Font("돋움", Font.PLAIN, 15);
		life_name_1 = new JLabel("              1");
		life_name_2 = new JLabel("              2");
		life_name_3 = new JLabel("              3");
		life_name_4 = new JLabel("              4");
		life_heart_1 = new JLabel(heart);
		life_heart_2 = new JLabel(heart);
		life_heart_3 = new JLabel(heart);
		life_heart_4 = new JLabel(heart);
		life_1_num = new JLabel("       10");
		life_2_num = new JLabel("       10");
		life_3_num = new JLabel("       10");
		life_4_num = new JLabel("       10");
		
		time = 30;
		timer = new JLabel("30 seconds");
		total_life = new JPanel();
		problem = new JLabel();

		input_line = new JTextField("Chat message input line",10);
		MessageArea = new JTextArea("");
		Message_pane = new JScrollPane();

		life_counter = 10;
		total_life.setLayout(new GridLayout(4,3,2,2));
		total_life.setBounds(1150, 450, 250, 130);
		total_life.setBackground(new Color(255,255,255));
		total_life.add(life_name_1);
		total_life.add(life_heart_1);
		total_life.add(life_1_num);
		total_life.add(life_name_2);
		total_life.add(life_heart_2);
		total_life.add(life_2_num);
		total_life.add(life_name_3);
		total_life.add(life_heart_3);
		total_life.add(life_3_num);
		total_life.add(life_name_4);
		total_life.add(life_heart_4);
		total_life.add(life_4_num);
		
		
		life_panel.setLayout(null);
		setlife(life_panel,life_arr,heart);
		life_panel.setBounds(1150, 600, 200, 68);
		life_panel.setBackground(new Color(245,209,183));

		JButton send_button = new JButton(send);
		send_button.setBounds(265,5,80,30);
		text_btn_panel.add(send_button);

		input_line.setEditable(true);
		input_line.setBounds(10,5,250,30);
		text_btn_panel.add(input_line);
		text_btn_panel.setLayout(null);
		text_btn_panel.setBounds(10, 280, 350, 40);
		text_btn_panel.setBackground(new Color(255,204,153));

		MessageArea.setBackground(new Color(255,204,153));
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
		chat_panel.setBackground(new Color(51,51,51));
		chat_panel.add(text_btn_panel);
		chat_panel.add(Message_pane);

		timer.setBounds(900,15,100,30);
		timer.setBorder(BorderFactory.createBevelBorder(1));
		timer.setForeground(Color.red);
		timer.setFont(new Font(Font.DIALOG, Font.ITALIC, 14));

		problem.setBounds(10,60,1000,250);
		problem.setBorder(null);
		problem.setIcon(temp);
				
		answers = new ArrayList<JButton>();
		answer_button_listener = new MouseListener()
		{
			public void mouseClicked(MouseEvent e) {
				System.out.println("Clicked!!!!!!");
				//client.setAnswer(answers.indexOf(e.getSource()) + 1); // index는 0부터 시작하므로 + 1을해줘서 정답 범위는 1 ~ 4 가 됨.
				card_panel.attack_result=answers.indexOf(e.getSource()) + 1;
				card_panel.setPressedButton(-1);
			}
			public void mouseEntered(MouseEvent e) {}
			public void mouseExited(MouseEvent e) {}
			public void mousePressed(MouseEvent e) {}
			public void mouseReleased(MouseEvent e) {}
		};
		for(i=0; i<4; i++)
		{
			answers.add(i,new JButton());
			Problem_panel.add(answers.get(i));
			answers.get(i).setBounds(150 + 200*i, 320, 100, 50);
			//answers.get(i).setEnabled(false);
			answers.get(i).addMouseListener(answer_button_listener);
		}
		answers.get(0).setIcon(one);
		answers.get(1).setIcon(two);
		answers.get(2).setIcon(three);
		answers.get(3).setIcon(four);
		
		Problem_panel.setLayout(null);
		Problem_panel.setBounds(50,50,1020,380);
		Problem_panel.setBackground(new Color(255,255,255));
		Problem_panel.add(timer);
		Problem_panel.setBorder(BorderFactory.createSoftBevelBorder(0));
		Problem_panel.add(problem);

		card_panel.setBounds(50,450,1060,250);
		this.setLayout(null);
		setBounds(250,150,1500,800);
		setBackground(new Color(51,51,51)); // 무슨 색깔로 하지...?
		add(total_life);
		add(life_panel);
		add(card_panel);
		add(chat_panel);
		add(Problem_panel);
		setVisible(true);
		//this.setResizable(false);
		//setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		//card_panel.setLocation(50,450);
		
		card_info = new ArrayList<Integer>(5);
		new_card_info = new ArrayList<Integer>(5);
		card_info.add(0); // addAll 로 수정가능하면 하기.
		card_info.add(0);
		card_info.add(0);
		card_info.add(0);
		card_info.add(0);
		
		//temp_panel = card_panel;
		card_exchange = new Exchange(card_panel);

		//채팅 입력창에 엔터키를 누르면 서버로 메시지가 전송된다.
		input_line.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				client.out.println("Message" +input_line.getText()+"");		
				input_line.setText("");
			}	
		});

		//채팅 입력창에 마우스 클릭하면 이미 기존에 있던 내용을 굳이 백스페이스바 누르면서 지울필요없이 한번에 없어진다.
		input_line.addMouseListener(new MouseListener() {
			public void mouseClicked(MouseEvent arg0) {
				input_line.setText("");
			}
			public void mouseEntered(MouseEvent arg0) {}
			public void mouseExited(MouseEvent arg0) {}
			public void mousePressed(MouseEvent arg0) {}
			public void mouseReleased(MouseEvent arg0) {}
		});

		//엔터키를 누르지 않아도 옆에있는 버튼을 클릭함으로써 같은 효과를 낼 수 있다.
		send_button.addMouseListener(new MouseListener(){

			public void mouseClicked(MouseEvent arg0) {
				client.out.println("Message" +input_line.getText()+"");	
				input_line.setText("");
			}
			public void mouseEntered(MouseEvent arg0) {}
			public void mouseExited(MouseEvent arg0) {}
			public void mousePressed(MouseEvent arg0) {}
			public void mouseReleased(MouseEvent arg0) {}

		});
		for(int i=0; i<7; i++) // 처음에 초기화 모두다 false로.
		{
			state[i] = false;	
		}
		logo[0] = logo_start.getImage();
		logo[1] = logo_turn.getImage();
		logo[2] = logo_attack.getImage();
		logo[3] = logo_correct.getImage();
		logo[4] = logo_wrong.getImage();
		logo[5] = logo_win.getImage();
		logo[6] = logo_lose.getImage();
		
		urls[0] = this.getClass().getClassLoader().getResource("music_back.wav");
		urls[1] = this.getClass().getClassLoader().getResource("attack.wav");
		urls[2] = this.getClass().getClassLoader().getResource("correct.wav");
		urls[3] = this.getClass().getClassLoader().getResource("wrong.wav");
		urls[4] = this.getClass().getClassLoader().getResource("win.wav");
		urls[5] = this.getClass().getClassLoader().getResource("lose.wav");
						
	}
		//1초씩 delay
		public void pause(int time){
		    try {
		      Thread.sleep(time);
		    } catch (InterruptedException e) { }
		}
		public int stopwatch(){
			card_panel.attack_result=0;
			card_panel.addEvent(2);
			while(timer_set>=0&&card_panel.attack_result==0){
				pause(1000);
				timer_set--;
				timer.setText(String.valueOf(timer_set)+" seconds.");
				if(timer_set==0){
					timer_set=30;
					timer.setText(String.valueOf(timer_set)+" seconds.");
					card_panel.dropEvent(2);
					return 9;
				}
			}
			timer_set=30;
			timer.setText(String.valueOf(timer_set)+" seconds.");
			card_panel.dropEvent(2);
			card_panel.useCard();
			return card_panel.attack_result;
		}
		
		public String whoStopwatch()
		{
			card_exchange.send_result=1;
			who_timer_set=30;
			String direction;
			card_panel.attack_result=0;
			//card_panel.dropEvent(1);
			//card_panel.addEvent(3);
			while(card_panel.attack_result==0 && who_timer_set>=0)
			{
				pause(1000);
				who_timer_set--;
				timer.setText(String.valueOf(who_timer_set)+" seconds.");	
				repaint();
			}		
			timer.setText("30 seconds.");
			card_exchange.send_result=0;
			card_panel.dropEvent(3);
			//card_panel.addEvent(1);
			System.out.println(who_timer_set);
			if(who_timer_set==-1)
			{
				System.out.println("Enter X");
				direction = "X";
				return direction;
			}
			else
			{
				System.out.println("Enter L and R");
				if(card_panel.attack_result == 1)
					return "L"+card_panel.useCard();
				else
					return "R"+card_panel.useCard();				
			}
		}
		
		//array가 시작 부분이 0인지 1인지 물어보기
		public void changLife(int[] array){
			for(int i=1;i<5;i++)
				aboutLife(i,array[i-1]);
		}
		

		public void aboutLife(int order, int life){
			if(order==1){
				life_1_num.setText("       "+String.valueOf(life));
				if(life==0)
					life_heart_1.setIcon(heart2);
			}
			else if(order==2){
				life_2_num.setText("       "+String.valueOf(life));
				if(life==0)
					life_heart_2.setIcon(heart2);
			}else if(order==3){
				life_3_num.setText("       "+String.valueOf(life));
				if(life==0)
					life_heart_3.setIcon(heart2);
			}else if(order==4){
				life_4_num.setText("       "+String.valueOf(life));
				if(life==0)
					life_heart_4.setIcon(heart2);
			}
		}
		
		public void SetMyLifeOrder(int order,String name){
			if(order==1)
				life_name_1.setText("              "+name);
			else if(order==2)
				life_name_2.setText("              "+name);
			else if(order==3)
				life_name_3.setText("              "+name);
			else if(order==4)
				life_name_4.setText("              "+name);
		}

	public void setlife(JPanel life_panel,JLabel life_arr[],ImageIcon heart) // initial setting
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

	public void update_life(int updated_life) // ActionListener call this method to update current life.
	   {      
	      int i;
	      int width = 40 , height = 34;

	      life_counter = updated_life;
	      for(i=life_counter; i<10; i++)
	      {
	         if(life_state[i] == true)
	            life_state[i] = false;
	         life_arr[i].setIcon(heart2);
	         life_arr[i].setBounds((i%5)*width,(i/5)*height,width,height);
	      }
	   }

	public void show_message(String str)
	{
		MessageArea.append(str+"\n");
	}
	
	public void timedown()
	{
		for(int i = 30; i>=0; i--)
		{
			timer.setText(i+" seconds");
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	public void make_info(String info_list)
	{
		new_card_info.clear();
		for(int i=0; i<info_list.length(); i++){
			new_card_info.add(Integer.valueOf(info_list.charAt(i) - '0'));
			System.out.println(new_card_info.get(i));
		}
	}
	public void exchangeOpen()
	   {
	      card_exchange.my_deck_set_info(card_panel.get_info());
	      card_exchange.new_deck_set_info(new_card_info);
	      card_exchange.openSet();
	      card_exchange.setVisible(true);
	   }
	
	public void start_on() // 시작하고 나서 이 음악 시작
	{
		try 
		{
			url = this.getClass().getClassLoader().getResource("music_back.wav");
			AudioInputStream audioIn = AudioSystem.getAudioInputStream(url);
			clip = AudioSystem.getClip();
			clip.open(audioIn);
			clip.start();
			clip.loop(clip.LOOP_CONTINUOUSLY);
		} catch (Exception ex) {
			System.out.println("sound exception");
		}
	}
	
	public void start_re_on()
	{
		temp_clip.close();
		clip.start();
	}
	public void music_on(int k)
	{
		try 
		{
			AudioInputStream audioIn = AudioSystem.getAudioInputStream(urls[k]);
			temp_clip = AudioSystem.getClip();
			temp_clip.open(audioIn);
			temp_clip.start();
			//if(!temp_clip.isOpen())
				//clip.start();
		} catch (Exception ex) {
			System.out.println("sound exception");
		}
	}
	public void music_change(int k)  // 모든 음악 끌 때 이 음악 사용
	{
		clip.stop(); // stop했다가 다시 start하면 멈춘 위치에서부터 다시 시작함
		music_on(k);
	}
	
	public void logo_on(int k)
	{
		state[k] = true;
		this.repaint();
		try {
			Thread.sleep(5000); // 5초동안 기다렸다가
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public void logo_off(int k)
	{
		state[k] = false;
		this.repaint();
	}
	
	public void paint(Graphics g)
	{
		super.paint(g);
		for(int i=0; i<7; i++)
		{
			if(state[i] == true){
				g.drawImage(logo[i], 600, 150,225,225, this);
				break;
			}
		}
		if(attacked == 1)
			g.drawImage(lock.getImage(), 1100, 50 , 370 , 345 , this);	
	}
	public void setAttack(int i)
	{
		attacked = i;
		if(attacked == 1) // Deck의 아이템 4,5버튼들도 활성화해주기.
		{
			input_line.setEditable(false);
			for(int k=0; k<4; k++)
				answers.get(k).setEnabled(true);
			//card_panel.addEvent(3);
		}
		else // Deck의 아이템 4,5버튼들 removelistener()해주기.
		{
			input_line.setEditable(true);
			/*for(int k=0; k<4; k++)
				answers.get(k).setEnabled(false);*/
			//card_panel.dropEvent(3);
		}	
	}
	public Clip getClip()
	{
		return temp_clip;
	}
	public String getLoot()
	{
		ArrayList<Integer> loot= card_panel.get_info();
		String result ="";
		for(i=0; i<5; i++)
			result = result + loot.get(i);
		return result;
	}
	public void setProblem(ImageIcon a)
	{
		problem.setIcon(a);
	    repaint();
	}
}