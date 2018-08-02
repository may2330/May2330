
import java.awt.Color;
import java.awt.Image;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import javax.swing.*;

public class Client  {

   BufferedReader in;
   PrintWriter out;
   
   private static JFrame frame;
   private Test temp;
   private ImageIcon icon = new ImageIcon("icon.png");
   private int answer = 0;
   private ImageIcon question[] = new ImageIcon[55];
   private int msgtime = 30;
   private ImageIcon back_frame;
   
   public Client(){
      temp = new Test(this);
      frame = new JFrame("나랏말싸미");
      frame.add(temp);
      frame.setBounds(250,150,1500,800);
      frame.setIconImage(icon.getImage());
      back_frame = new ImageIcon("back2.jpg");
   };
// 테더링 스마트폰 테더링 테스트할 때
   private String getServerAddress() {
      return JOptionPane.showInputDialog(
            frame,
            "Enter IP Address of the Server:",
            "Welcome to the Chatter",
            JOptionPane.QUESTION_MESSAGE);
   }

   /**
    * Prompt for and return the desired screen name.
    */
   private String getName() {
      return JOptionPane.showInputDialog(
            frame,
            "Choose a screen name:",
            "Screen name selection",
            JOptionPane.PLAIN_MESSAGE);
   }


   private void run() throws IOException {

      String serverAddress = getServerAddress();
      Socket socket = new Socket(serverAddress, 9001);
      in = new BufferedReader(new InputStreamReader(
            socket.getInputStream()));
      out = new PrintWriter(socket.getOutputStream(), true);

      for(int i=0; i<55; i++)
      {
         ImageIcon temp_icon = new ImageIcon("question/"+(i+1)+".png");
         Image temp = temp_icon.getImage().getScaledInstance(1000, 250, 2);
         question[i] = new ImageIcon(temp);
      }
      
      while (true) {
         String line = in.readLine();
         System.out.println("I got this :: "+line);
         if (line.startsWith("SUBMITNAME")) {
            out.println(getName());
         } else if (line.startsWith("NAMEACCEPTED")) {
            frame.setVisible(true);
         } else if (line.startsWith("Broadcast")) {
            temp.show_message(line.substring(9));   
         //   System.out.println("ATTACK"+temp.whoStopwatch());
         } else if (line.startsWith("SEND")){
            temp.make_info(line.substring(4));
            temp.exchangeOpen();
         } else if (line.startsWith("START")){
            temp.start_on();
            temp.logo_on(0);  // 로고를 켰다가
            temp.logo_off(0);  // 로고를 끈다.
         }else if (line.startsWith("ORDER")) {
            temp.SetMyLifeOrder(line.charAt(5) - '0', line.substring(6));
         } else if (line.startsWith("WHO")) {
            temp.setAttack(1);
            out.println("ATTACK"+temp.whoStopwatch());
            temp.setAttack(0);
         } else if (line.startsWith("ATK")) {
               temp.setAttack(1); // 자물쇠 이미지를 채팅창에 덮어서 안보이게 아기 또는 inpt_text 로 대화못보내게 하기
               temp.music_change(1); // 공격받았을 때 음악 틀기, ***********
               temp.logo_on(2);// 공격받았다는 로고 띄우기
               temp.logo_off(2); // 로고를 끈다.
               temp.setProblem(question[Integer.valueOf(line.substring(3))]);
               answer = temp.stopwatch();
               if(answer>=1&&answer<=4)//answer
                  out.println("ANSWER"+answer);
               else if(answer==5)//use item
                  out.println("USE"+(answer-1)+"L");
               else if(answer==6)//use item
                  out.println("USE"+(answer-2)+"F");
               else if(answer==7)//use item
                  out.println("USE"+(answer-3)+"R");
               else if(answer==8)//use item
                  out.println("USE"+(answer-3));
               else{//time out
                  out.println("ANSWER0");
               }
               temp.start_re_on(); // 다시 배경음악을 킨다.
               temp.setAttack(0);
               answer = 0;
            } else if (line.startsWith("NATK")) {
               temp.setProblem(question[Integer.valueOf(line.substring(4))]);    
         } else if (line.startsWith("CORRECT")) {
            temp.music_change(2); // 맞았다는 음악 잠깐 틀어주기 띄링~
            temp.logo_on(3);// correct 로고 띄어주기
            temp.logo_off(3);
            //while(temp.getClip().isOpen()){}; // 맞았다는 효과음 끝날 때가지 기다렸다가
            temp.start_re_on(); // 멈췄던 부분부터 다시 배경음악을 킨다
            out.println("DROP_NATK");
            out.println("ACK");         
         } else if (line.startsWith("WRONG")) {
            temp.music_change(3);
            temp.logo_on(4);
            temp.logo_off(4);
            temp.update_life(Integer.valueOf(line.substring(5)));
            //while(temp.getClip().isOpen()){}; // 틀렸다는 효과음 끝날 때가지 기다렸다가
            temp.start_re_on(); // 멈췄던 부분부터 다시 배경음악을 킨다
            out.println("DROP_NATK");
            out.println("ACK");
         } else if (line.startsWith("LOSE")) {
            temp.update_life(0);
            temp.music_change(5); // 죽었다는 음악재생
            temp.logo_on(6);// 졋다는 로고 띄어주기
            temp.logo_off(6);
            out.println("DROP_NATK");
            out.println("LOOT"+temp.getLoot()); // 내 덱에 남아있는 card_info를 string형태로 변환해서 서버에게 보내주기    공격자의 전리품   
         } else if (line.startsWith("YOUR_TURN")) {
            temp.logo_on(1);
            temp.logo_off(1);
            out.println("TURN_ACK");
         } else if (line.startsWith("WIN")) {
            temp.music_change(4); // 이겼다는 음악재생
            temp.logo_on(5); // 이겼다는 이미지 로고 띄어주기
            // 게임 끝
         } else if (line.startsWith("DROP_NATK")) {
            temp.setProblem(back_frame);
         } else if (line.startsWith("LIST")) {
            temp.aboutLife(line.charAt(4) - '0', line.charAt(5)-'0');
            // 진행창 이미지 업데이트 해주기
            // 바뀐 유저의 LABEL부분에 border를 깜빡깜빡 켰다 껐다를 반복하는 함수를 실행시키고 몇초후에 그 함수 꺼버리기
            // 음악 넣을거 있으면 넣기 띠릥~
         }
      }
   }
   
   public static void main(String[] args) throws Exception{
      Client client = new Client();   
      client.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      client.run();
   }
   
   public void setAnswer(int k)
   {
      answer = k;
   }
   
   
}