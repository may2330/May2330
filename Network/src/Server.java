import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.KeyStore.Entry;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;



public class Server {
	private static int client_count =0;
	private static int turn = 1;
	private static int attack_turn = 0;
	private static int problem_number = 1;
	private static ArrayList<Integer> life_list = new ArrayList<Integer>();
	private static int timer=30;
   private static int[] question_answer = {1,3,1,3,2,4,2,2,1,4,3,3,1,1,1,4,1,3,1,1,1,2,4,1,
	            4,3,3,2,2,4,3,1,4,1,4,2,4,1,3,3,2,2,4,4,4,3,2,4,4,2,4,4,4,4,2};
	private static final int PORT = 9001;
	private static HashSet<String> names = new HashSet<String>();

 
    private static HashMap<PrintWriter,Integer> writers = new HashMap<PrintWriter,Integer>();
    private static ArrayList<Integer> client_array = new ArrayList<Integer>();

    public static void main(String[] args) throws Exception {
        System.out.println("The chat server is running.");
        ServerSocket listener = new ServerSocket(PORT,4);

        try {
            while (true) {
                new Handler(listener.accept()).start();
            }
        } finally {
            listener.close();
        }
    }


    private static class Handler extends Thread {
        private String name;
        private Socket socket;
        private BufferedReader in;
        private PrintWriter out;
        private int client_number;
        private int life;

        public Handler(Socket socket) {
            this.socket = socket;
        }

        
        public void run() {
        	
            try {
               if(client_count==4){
                  socket.close();
               }
               
               client_count = client_count +1;
                in = new BufferedReader(new InputStreamReader(
                    socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);
                life = 5;

                while (true) {
                    out.println("SUBMITNAME");
                    name = in.readLine();
                    
                    if (name == null) {
                        return;
                    }
                    synchronized (names) {
                        if (!names.contains(name)) {
                            names.add(name);
                            break;
                        }
                    }
                }

                out.println("NAMEACCEPTED");
                writers.put(out,client_count);
                client_array.add(client_count);
                life_list.add(life);
                client_number = client_count;
                     
                for (PrintWriter writer : writers.keySet())  // 한 명 씩 들어올 때마다 메시지창에 누가 들어왔는지 broadcast 해줌
                    writer.println("Broadcast"+"<SYSTEM>"+ name+" entered");
                				
                if(client_count == 4) // 마지막 한 명이 들어올 때 start 버튼을 눌러서 다른 모든 thread의 out으로 메시지를 보냄.
                {
                	int i=1;
                	for(PrintWriter writer : writers.keySet())
                	{
                		PrintWriter next = getOut(i);
                		next.println("ORDER"+i+"ME");
                		i++;
                	}
                	
                	for(PrintWriter writer : writers.keySet())
                	{
                		writer.println("START"); // 1번 2번 3번 카드는 각각 Level 1~3의 카드를 의미함. 처음 시작할 때 모두에게 3장식 랜덤으로 부여하고 시작
                		writer.println("SEND"+setCardNumber()+setCardNumber()+setCardNumber());
                	}
                	PrintWriter next = getOut(turn);
            		next.println("YOUR_TURN");
                }
                /*
                out.println("START"+"1"+name);
                out.println("SEND"+1+2+3);
                 try {
					Thread.sleep(15000);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}*/
                 //out.println("YOUR_TURN"); 
                //out.println("ATK");
                while (true) 
                {
                    String input = in.readLine();
                    System.out.println("input :"+input);
                    if (input == null)
                        return;
                    else if(input.startsWith("Message")) 
                    {
                    	for (java.util.Map.Entry<PrintWriter, Integer> writer : writers.entrySet()) 
                    	{
                    		if(writer.getValue() != attack_turn) // 현재 문제를 풀고있는 attack_turn은 대화를 할 수 없다.
                    			writer.getKey().println("Broadcast" + name + ": " + input.substring(7));
                        }                       
                    }
                    else if(input.startsWith("TURN_ACK")){ // 오로지 YOUR_TURN을 받은 client만 TURN_ACK을 보냄. 응 내차례구나 알았어~
                    	out.println("WHO");
                    	attack_turn = 0;
                    }
                    else if(input.startsWith("ATTACK")) // ATTACKL3 // 왼쪽유저에게 3 난이도 카드로 공격!
                    {
                    	System.out.println(input);
                         char direction = input.charAt(6); // L or R
                         if(direction == 'L')
                            attack_turn = getLeft(getIndex(turn));
                         else if(direction == 'R')
                            attack_turn = getRight(getIndex(turn));
                         else // direction == 'X'  방향없음. 누구 공격할지 turn넘겨줘서 기회줬는데 아무도 선택안함
                         {
                            turn = getTurn(getIndex(turn)+1);  // 다음 턴으로 이동!
                             PrintWriter next = getOut(turn);
                             next.println("YOUR_TURN");
                             next.println("SEND"+setCardNumber());
                             continue;
                         }
                         
                         setProblemNumber(input.charAt(7) - '0');
                       for (java.util.Map.Entry<PrintWriter, Integer> writer : writers.entrySet()) 
                         {
                            if(writer.getValue() == attack_turn)  // timer작동시켜주기
                               writer.getKey().println("ATK"+problem_number);  //random한 문제골라서 주기.
                            else
                               writer.getKey().println("NATK"+problem_number); // 얘도 마찬가지로 아까 선택된 random한 문제 주기.
                          } 
                      }
                    else if(input.startsWith("USE"))  //example : USE4F OR USE5
                    {
                    	if(input.charAt(3)-'0' == 5) // reflect card
                    	{
                    		attack_turn = turn;
                    		for (java.util.Map.Entry<PrintWriter, Integer> writer : writers.entrySet()) 
                        	{
                        		if(writer.getValue() == attack_turn)  // timer작동시켜주기
                        			writer.getKey().println("ATK"+problem_number);  //turn_input(7)에 의해 random한 문제골라서 주기.
                        		else
                        			writer.getKey().println("NATK"+problem_number); // 얘도 마찬가지로 아까 선택된 random한 문제 주기.
                            } 
                    		
                    	}
                    	else
                    	{
                    		char direction = input.charAt(4);
                    		if(direction == 'L')
                        		attack_turn = getLeft(getIndex(attack_turn));
                        	else if(direction == 'R')
                        		attack_turn = getRight(getIndex(attack_turn));
                        	else
                        		attack_turn = getForward(getIndex(attack_turn));
                        	
                			for (java.util.Map.Entry<PrintWriter, Integer> writer : writers.entrySet()) 
                        	{
                        		if(writer.getValue() == attack_turn)  // timer작동시켜주기
                        			writer.getKey().println("ATK"+problem_number);  //turn_input(7)에 의해 random한 문제골라서 주기.
                        		else
                        			writer.getKey().println("NATK"+problem_number); // 얘도 마찬가지로 아까 선택된 random한 문제 주기.
                            } 
                    	}
                    }
                    else if(input.startsWith("ANSWER"))  // life_list 최신화해주고 넘겨주기~!!!!!!!!!!
                    {
                    	if(input.charAt(6) - '0' == question_answer[problem_number - 1]) // 정답비교
                    		out.println("CORRECT");
                    	else
                    	{
                    		life = life - getDifficulty(); //  난이도가 1인지 2인지 3인지에 따라 마이너스 해줌.
                    		if(life > 0)
                    		{
                    			life_list.set(getIndex(attack_turn), life); 
                    			out.println("WRONG"+life);
                    		}
                    		else
                    		{
                    			life_list.set(getIndex(attack_turn), 0);
                    			out.println("LOSE");
                    		}
                    	
                    	for(PrintWriter writer : writers.keySet())  // 예를들면 LIST27 : 2번째 유저의 라이프는 7개로 줄어듬!
                    		writer.println("LIST"+attack_turn+life_list.get(getIndex(attack_turn))); // 틀린 클라이언트의 변화된 life를 업데이트 해준다.
                    	}
                    }
                    else if(input.startsWith("ACK")) // CORRECT 또는 WRONG을 받은 CLIENT가 보낸 메시지 // (CORRECT,WRONG) -> ACK -> 다음차례
                    {
                    	
                    	turn = getTurn(getIndex(turn)+1);
                    	PrintWriter next = getOut(turn);
                    	next.println("YOUR_TURN");
                    	next.println("SEND"+setCardNumber());
                    } 
                    else if(input.startsWith("DROP_NATK")) // CORRECT 또는 WRONG을 받은 CLIENT가 보낸 메시지 // (CORRECT,WRONG) -> ACK -> 다음차례
                    {
                    	for(PrintWriter writer : writers.keySet())
                    		writer.println("DROP_NATK");
                    }
                    else if(input.startsWith("LOOT")) // LOSE 를 받은 CLIENT가 보낸 메시지 // (LOSE) -> LOOT -> 다음차례
                    {
                    	getOut(turn).println("SEND"+input.substring(4));     
                    	extractArray(getIndex(attack_turn));
                    	
                    	if(client_count != 1)
                    	{
                    		turn = getTurn(getIndex(turn)+1);
                    		PrintWriter next = getOut(turn);
                    		next.println("YOUR_TURN");
                    		next.println("SEND"+setCardNumber());
                    	}
                    	else
                    	{
                    		getOut(turn).println("WIN");
                    		break; // 게임 끝!
                    	}      		
                    }
                }              
            } catch (IOException e) {
                System.out.println(e);
            } finally {
                if (name != null) {
                    names.remove(name);
                }
                if (out != null) {
                    writers.remove(out);
                }
                try {
                    client_count --;
                    socket.close();
                } catch (IOException e) {
                }
            }
        }
    }
    private static int getLeft(int array_index) //현재 turn인 유저의 index를 받고 그 왼쪽에 위치한 유저의 고유 ID를 return해준다.
    {
    	if(array_index == 0)
    		return client_array.get(client_array.size()-1); // index부분이므로 크기 - 1을 해줘야한다.
    	else
    		return client_array.get(array_index-1);
    } 
    
    private static int getRight(int array_index)
    {
    	if(array_index == client_array.size()-1)
    		return client_array.get(0);
    	else
    		return client_array.get(array_index+1);
    }
    
    private static int getForward(int array_index)
    {
    	int enemey_index = (array_index + 2) % client_count;
    	if(enemey_index == array_index)
    		return getRight(array_index); // default
    	else
    		return client_array.get(enemey_index);
    }
    
    private static void extractArray(int array_index) //공격받은 attack_turn의 index를 받아서 더이상 그가 게임에 참여하지 못하도록 turn이 넘어가도 차례가오지않게 client_array에서 빼줌
    {
    	client_array.remove(array_index);
    	life_list.remove(array_index);
    	client_count--;
    }
    
    
    private static PrintWriter getOut(int turn_num)
    {
    	for (java.util.Map.Entry<PrintWriter, Integer> writer : writers.entrySet())
    	{
    		if(turn_num == writer.getValue())
    		{
    			return writer.getKey();
    		}
    	}
		return null;
    }
    private static void setProblemNumber(int difficulty)
    {
    	Random generator = new Random();
    	if(difficulty == 1)
    		problem_number =  generator.nextInt(29)+1;  // 1 ~ 30 사이를 랜덤으로 선택 후 return
    	else if(difficulty == 2)
    		problem_number =  generator.nextInt(19)+31;  // 31 ~ 50사이를 랜덤으로 선택 후 return
    	else
    		problem_number =  generator.nextInt(4)+51; // 51 ~ 55 사이를 랜덤으로 선택 후 return
    }
    
    private static int setCardNumber(){
    	Random generator = new Random();
    	//generator.setSeed(System.currentTimeMillis());
    	int cardNumber = generator.nextInt(4)+1;
    	return cardNumber;
    }
    
    private static int getDifficulty()
    {
    	if(problem_number <= 30)
    		return 1;
    	else if(problem_number <= 50)
    		return 2;
    	else
    		return 3;
    }

    private static int getIndex(int turnNum){
    	for(int i=0;i<client_array.size();i++){
    		if(client_array.get(i)==turnNum)
    			return i;
    	}
    	return 0;
    }
    
    private static int getTurn(int Index){
    	if(Index==client_array.size())
    		return client_array.get(0);
    	return client_array.get(Index);
    }
}