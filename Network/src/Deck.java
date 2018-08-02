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
            if(card_info.get(buttons.indexOf(e.getSource())) == 5) // �ݻ�ī�崭���� ���� attack_result�� 8�� ����
               attack_result=8;
            else // ����ī�崭���� ���� return_point()�Լ� ���ؼ� â�� �ߵ��� �ؾ� ��.
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
   
   public void Insert(int card_id) // 1 ~ 3 �� Level 1,2,3 �� �ǹ�. 4�� point 5�� reflect card�� �ǹ�.
   {
      for(int k=0; k<card_max; k++)
      {
         if(isZero(k)) // for���� ������ ���� ī�帮��Ʈ�߿��� ���� ó������ ���� ������ٰ� ���ο� ī�带 �������.
         {
            card_info.set(k,card_id);
            break;
         }
      }
      reset(); // ī�嵦 ������ �������Ƿ� ���� �������� �̹��� �籸��.
   }
   
   public void Delete(int k) // card_info array���� k��°�� �ִ� ī�带 ������.
   {
      card_info.set(k, 0);
      buttons.get(k).setIcon(back); // �� ���� ī���̹����� ����.
   }
   
   public boolean isZero(int i) // card info array���� i���� ��ġ�� ī�尡 �ֳ� ������ üũ
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
   
   public int send(int k) // ī�嵦���� k��° ī�带 �����ؼ� �����°� �ƴ϶� ���� �������� ���ְ� �ٸ� ���� return���ֱ� ���ؼ� ���� �Լ�
   {
      int temp = card_info.get(k);
      Delete(k);
      return temp;
   }
   
   public ArrayList<Integer> get_info() // ���� ���� �������ִ� ���¸� return ���ش�.
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
      if(type == 1) // exchange open�� �� add / drop �� �� �ֵ��� ���� event ó���� �ֱ�.
      {
         for(i=0; i<card_max; i++)
            buttons.get(i).addMouseListener(mouse_handler);         
      }
      else if(type == 2) // ����ī�常 ����ϵ��� �ϱ�
      {
         System.out.println("Enter type2 - add");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 4 || card_info.get(i) == 5){
               buttons.get(i).removeMouseListener(mouse_handler);
               buttons.get(i).addMouseListener(point_listener);}
         }
      }
      else if(type == 3) // ����ī�常 ������ΤǤ� �ϱ�
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
      if(type == 1) // exchange open�� �� add / drop �� �� �ֵ��� ���� event ó���� �ֱ�.
      {
         for(i=0; i<card_max; i++){
            buttons.get(i).removeMouseListener(mouse_handler);}   
      }
      else if(type == 2) // ����ī�常 ����ϵ��� �ϱ�
      {
         System.out.println("Enter type2 - drop");
         for(i=0; i<card_max; i++)
         {
            if(card_info.get(i) == 4 || card_info.get(i) == 5){
               buttons.get(i).removeMouseListener(point_listener);
            buttons.get(i).addMouseListener(mouse_handler);}
         }
      }
      else if(type == 3) // ����ī�常 ������ΤǤ� �ϱ�
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
      String[] buttons = {"����", "�ǳ���", "������"};
      int result = JOptionPane.showOptionDialog(null, "�������� ����?", "����â", JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE, null, buttons, "����");
      if(result==JOptionPane.YES_OPTION)
         attack_result=5;
      else if (result==JOptionPane.NO_OPTION)
         attack_result=6;
      else 
         attack_result=7;
   }
   public void return_attack(){
      String[] buttons = {"����", "������"};
      int result = JOptionPane.showOptionDialog(null, "�������� ����?", "����â", JOptionPane.YES_NO_OPTION, JOptionPane.PLAIN_MESSAGE, null, buttons, "����");
      if(result==JOptionPane.YES_OPTION)
         attack_result=1;
      else if (result==JOptionPane.NO_OPTION)
         attack_result=2;
   }
     public int useCard()  // ������!!!!
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