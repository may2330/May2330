import java.awt.Color;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.net.URL;
import java.util.ArrayList;

import javax.swing.AbstractButton;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.event.AncestorListener;

public class Deck extends JPanel{

   private static final int card_max = 5;
   private static final int card_width = 200;
   private static final int card_height = 230;
   private int card_num;
   private ArrayList<JButton> buttons;
   private ArrayList<Integer> card_info;
   private ImageIcon back = new ImageIcon("back.jpg");
   private ImageIcon one = new ImageIcon("Level1.png");
   private ImageIcon two = new ImageIcon("Level2.png");
   private ImageIcon three = new ImageIcon("Level3.png");
   private ImageIcon point = new ImageIcon("Point.png");
   private ImageIcon reflect = new ImageIcon("Reflect.png");
   
   private int i;
   private int pressed_button;
   private long pressed_time;
   public int attack_result = 0;
   
   private MouseListener mouse_handler = new MouseListener()
   {
      public void mouseClicked(MouseEvent e) {
         pressed_button = buttons.indexOf(e.getSource());
         pressed_time = e.getWhen();
      }
      public void mouseEntered(MouseEvent e) {
         ((JComponent) e.getSource()).setBorder(BorderFactory.createLineBorder(Color.RED, 3));
      }
      public void mouseExited(MouseEvent e) {((JComponent) e.getSource()).setBorder(null);}
      public void mousePressed(MouseEvent e) {}
      public void mouseReleased(MouseEvent e) {}
   };
   
    private MouseListener point_listener = new MouseListener()
      {
         public void mouseClicked(MouseEvent e) {
            pressed_button = buttons.indexOf(e.getSource());
            if(card_info.get(buttons.indexOf(e.getSource())) == 5) // 반사카드눌렀을 때만 attack_result를 8로 설정
               attack_result=8;
            else // 지목카드눌렀을 때만 return_point()함수 콜해서 창이 뜨도록 해야 함.
               return_point();
         }
         public void mouseEntered(MouseEvent e) {
            ((JComponent) e.getSource()).setBorder(BorderFactory.createLineBorder(Color.RED, 3));
         }
         public void mouseExited(MouseEvent e) {((JComponent) e.getSource()).setBorder(null);}
         public void mousePressed(MouseEvent e) {}
         public void mouseReleased(MouseEvent e) {}
      };
      
   private MouseListener card_listener = new MouseListener()
   {
      public void mouseClicked(MouseEvent e) {
         pressed_button = buttons.indexOf(e.getSource());
         return_attack();
      }
      public void mouseEntered(MouseEvent e) {
         ((JComponent) e.getSource()).setBorder(BorderFactory.createLineBorder(Color.RED, 3));
      }
      public void mouseExited(MouseEvent e) {((JComponent) e.getSource()).setBorder(null);}
      public void mousePressed(MouseEvent e) {}
      public void mouseReleased(MouseEvent e) {}
   };
   
   public Deck()
   {

      card_num = 0;
      card_info = new ArrayList<Integer>();
      buttons = new ArrayList<JButton>();

      for(i=0; i<card_max; i++)
      {
         card_info.add(i,0);
         buttons.add(i,new JButton(back));
         this.add(buttons.get(i));
         buttons.get(i).setBounds(i*210+10, 10, card_width, card_height);
         //buttons.get(i).addMouseListener(mouse_handler);         
      }
      this.setLayout(null);
      this.setBounds(50, 450, 1060, 250);
      this.setBackground(new Color(051,051,051));
      this.setBorder(BorderFactory.createSoftBevelBorder(0));
   }
   
   public void Insert(int card_id) // 1 ~ 3 은 Level 1,2,3 을 의미. 4는 point 5는 reflect card를 의미.
   {
      for(int k=0; k<card_max; k++)
      {
         if(isZero(k)) // for문을 돌려서 현재 카드리스트중에서 가장 처음으로 오는 빈곳에다가 새로운 카드를 집어넣음.
         {
            card_info.set(k,card_id);
            break;
         }
      }
      reset(); // 카드덱 구성이 변했으므로 변한 구성으로 이미지 재구성.
   }
   
   public void Delete(int k) // card_info array에서 k번째에 있는 카드를 버린다.
   {
      card_info.set(k, 0);
      buttons.get(k).setIcon(back); // 빈 뒷장 카드이미지로 변경.
   }
   
   public boolean isZero(int i) // card info array에서 i번재 위치에 카드가 있나 없나를 체크
   {
      if(card_info.get(i) == 0)
         return true;
      else
         return false;
   }
   
   public void reset()
   {
      for(int k=0; k<card_max; k++)
      {
         switch(card_info.get(k))
         {
         case 0 : buttons.get(k).setIcon(back); break;
         case 1 : buttons.get(k).setIcon(one); break;
         case 2 : buttons.get(k).setIcon(two); break;
         case 3 : buttons.get(k).setIcon(three); break;
         case 4 : buttons.get(k).setIcon(point); break;
         case 5 : buttons.get(k).setIcon(reflect); break;
         }
      }
   }
   
   public int send(int k) // 카드덱에서 k번째 카드를 삭제해서 버리는게 아니라 현재 덱에서는 없애고 다른 덱에 return해주기 위해서 만든 함수
   {
      int temp = card_info.get(k);
      Delete(k);
      return temp;
   }
   
   public ArrayList<Integer> get_info() // 현재 덱이 가지고있는 상태를 return 해준다.
   {
      return card_info;
   }
   
   public void set_info(ArrayList<Integer> temp)
      {
         for(int i=0; i<temp.size(); i++)
            card_info.set(i, temp.get(i));
         for(int i=temp.size(); i<5; i++)
            card_info.set(i, 0);
      }
   public int get_pressed_button()
   {
      return pressed_button;
   }
   public long get_pressed_time()
   {
      return pressed_time;
   }
   public void addEvent(int type) 
   {
      if(type == 1) // exchange open할 때 add / drop 할 수 있도록 넣은 event 처리문 넣기.
      {
         for(i=0; i<card_max; i++)
            buttons.get(i).addMouseListener(mouse_handler);         
      }
      else if(type == 2) // 지목카드만 사용하도록 하기
      {
         System.out.println("Enter type2 - add");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 4 || card_info.get(i) == 5){
               buttons.get(i).removeMouseListener(mouse_handler);
               buttons.get(i).addMouseListener(point_listener);}
         }
      }
      else if(type == 3) // 공격카드만 사용핟로ㅗㄱ 하기
      {
         System.out.println("Enter type3 - add");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 1 || card_info.get(i) == 2 || card_info.get(i) == 3){
               buttons.get(i).removeMouseListener(mouse_handler);
               buttons.get(i).addMouseListener(card_listener);      }
         }
      }
   }   
   public void dropEvent(int type)  
   {
      if(type == 1) // exchange open할 때 add / drop 할 수 있도록 넣은 event 처리문 넣기.
      {
         for(i=0; i<card_max; i++){
            buttons.get(i).removeMouseListener(mouse_handler);}   
      }
      else if(type == 2) // 지목카드만 사용하도록 하기
      {
         System.out.println("Enter type2 - drop");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 4 || card_info.get(i) == 5){
               buttons.get(i).removeMouseListener(point_listener);
            buttons.get(i).addMouseListener(mouse_handler);}
         }
      }
      else if(type == 3) // 공격카드만 사용핟로ㅗㄱ 하기
      {
         System.out.println("Enter type3 - drop");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 1 || card_info.get(i) == 2 || card_info.get(i) == 3 || card_info.get(i) == 0)
            {
               System.out.println(i+"\n");
               buttons.get(i).removeMouseListener(card_listener);
               buttons.get(i).addMouseListener(mouse_handler);
            }
         }
      }
   }
   public void return_point(){
      String[] buttons = {"왼쪽", "건너편", "오른쪽"};
      int result = JOptionPane.showOptionDialog(null, "누구한테 공격?", "공격창", JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE, null, buttons, "왼쪽");
      if(result==JOptionPane.YES_OPTION)
         attack_result=5;
      else if (result==JOptionPane.NO_OPTION)
         attack_result=6;
      else 
         attack_result=7;
   }
   public void return_attack(){
      String[] buttons = {"왼쪽", "오른쪽"};
      int result = JOptionPane.showOptionDialog(null, "누구한테 공격?", "공격창", JOptionPane.YES_NO_OPTION, JOptionPane.PLAIN_MESSAGE, null, buttons, "왼쪽");
      if(result==JOptionPane.YES_OPTION)
         attack_result=1;
      else if (result==JOptionPane.NO_OPTION)
         attack_result=2;
   }
     public int useCard()  // 수정됨!!!!
      {
         if(pressed_button != -1)
         {
            int return_value = card_info.get(pressed_button);
            Delete(pressed_button);
            pressed_button = 0;
            reset();
            return return_value;
         }
         return 0;
      }
      public void setPressedButton(int temp)
      {
         pressed_button = temp;
      }
}