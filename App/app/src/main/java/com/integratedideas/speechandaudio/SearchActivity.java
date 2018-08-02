package com.integratedideas.speechandaudio;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.media.AudioManager;
import android.media.SoundPool;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.AudioEvent;
import be.tarsos.dsp.AudioProcessor;
import be.tarsos.dsp.io.android.AudioDispatcherFactory;
import be.tarsos.dsp.pitch.PitchDetectionHandler;
import be.tarsos.dsp.pitch.PitchDetectionResult;
import be.tarsos.dsp.pitch.PitchProcessor;

public class SearchActivity extends Activity {
        public static final String TAG = "ANDROID INSTRUMENTS"; //태그
        public static final int KEY_MARGIN = 1; // 건반간 간격 픽셀
        public static final int KEY_LENGTH = 7; // C Major 스케일 음계의 수
        public static final int OCTAVE_COUNT = 6; // 옥타브 수
        public static final String KEYS = "cdefgab"; // C Major 스케일 음계
        public static final String[] PITCHES = new String[]{"c", "cs", "d", "ds", "e", "f", "fs", "g", "gs", "a", "as", "b"}; // Chromatic 스케일 음계

        private ViewGroup viewKeys, keysContainer, swipeArea;
        private ImageView imgKey;

        private SoundPool sPool; // 사운드 풀
        private Map<String, Integer> sMap;
        private AudioManager mAudioManager;

        private int imgKeyWidth, programNo, octaveShift;
        private SharedPreferences pref; //앱을 사용할때 저장되어야하는 데이터들 (로그인 같은거)

        TextView text,text2,text3,text4,text5;
        Button button;
        TextView r1,r2,r3;
        private int r_left,r_right;
        private float pre_voice, after_voice,pre,voice;
        private int di_top,di_bottom;
        private AlertDialog.Builder ad;

        private ArrayList<Integer> notes;

        /** Called when the activity is first created. */
        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            pref = getSharedPreferences("test", Activity.MODE_PRIVATE);

            setContentView(R.layout.activity_search);

            r1 = (TextView)findViewById(R.id.r1);
            r2 = (TextView)findViewById(R.id.r2);
            r3 = (TextView)findViewById(R.id.r3);
            r_left = 0;
            r_right=0;
            pre_voice = -1;
            after_voice = -1;
            voice=-1;
            pre=-1;
            notes = new ArrayList<Integer>();
            di_bottom=0;
            di_top=0;

            notes.add(32);
            notes.add(36);
            notes.add(41);
            notes.add(43);
            notes.add(48);
            notes.add(55);
            notes.add(61);

            r1.setWidth(100);

            text = (TextView)findViewById(R.id.text);
            text2 = (TextView)findViewById(R.id.text2);
            text3 = (TextView)findViewById(R.id.text3);
            text4= (TextView)findViewById(R.id.text4);
            text5 = (TextView)findViewById(R.id.text5);

            AudioDispatcher dispatcher = AudioDispatcherFactory.fromDefaultMicrophone
                    (22050, 1024, 0);
            PitchDetectionHandler pdh = new PitchDetectionHandler() {
                @Override
                public void handlePitch(PitchDetectionResult result, AudioEvent e) {
                    final float pitchInHz = result.getPitch();
                    if(pitchInHz != -1)
                        pre_voice = pitchInHz;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            text.setText("" +  pre_voice);
                            text2.setText("" +  pre_voice);
                            text3.setText("" + pre_voice);
                            text4.setText("" + pre_voice);
                            text5.setText("" +  pre_voice);
                        }
                    });
                }
            };
            AudioProcessor p = new PitchProcessor(PitchProcessor.PitchEstimationAlgorithm.FFT_YIN, 22050, 1024, pdh);
            dispatcher.addAudioProcessor(p);
            new Thread(dispatcher, "Audio Dispatcher").start();

            viewKeys = (ViewGroup) findViewById(R.id.view_key);
            viewKeys.setOnTouchListener(keysTouchListener);

            keysContainer = (ViewGroup) findViewById(R.id.keys_container);
            keysContainer.setOnTouchListener(keysContainerTouchListener);
            int viewKeysScrollX = pref.getInt("viewKeysScrollX", 0);
            if(viewKeysScrollX>0)((HorizontalScrollView)viewKeys).smoothScrollTo(viewKeysScrollX, 0);

            imgKey = (ImageView) findViewById(R.id.img_key);
            imgKeyWidth = pref.getInt("imgKeyWidth", 4000);
            imgKey.setLayoutParams(new LinearLayout.LayoutParams(imgKeyWidth, LinearLayout.LayoutParams.FILL_PARENT));

            swipeArea = (ViewGroup) findViewById(R.id.swipe_area);

            resetSoundPool();
            mAudioManager = (AudioManager)getSystemService(AUDIO_SERVICE);

            boolean isFirstExec = pref.getBoolean("isFirstExec", true);
            if(isFirstExec){
                SharedPreferences.Editor editor = pref.edit();
                editor.putBoolean("isFirstExec", false);
                editor.commit();
            }

        }


        private View.OnTouchListener keysTouchListener = new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent event) {


                int action = event.getAction();
                int downPointerIndex = -1;

                if (action == MotionEvent.ACTION_DOWN) downPointerIndex = 0;
                else if(action == MotionEvent.ACTION_POINTER_DOWN) downPointerIndex = 0;
                else if(action == MotionEvent.ACTION_POINTER_1_DOWN) downPointerIndex = 0;
                else if(action == MotionEvent.ACTION_POINTER_2_DOWN) downPointerIndex = 1;
                else if(action == MotionEvent.ACTION_POINTER_3_DOWN) downPointerIndex = 2;

                int scrollAreaBottom = swipeArea.getBottom(); // 스크롤 영역의 하단

                if(downPointerIndex>=0){
                    int scrollWidth = keysContainer.getRight(); // 스크롤 폭
                    int keyWhiteWidth = (int) (((float) scrollWidth) / (KEY_LENGTH * OCTAVE_COUNT)); // 건반 하나당 할당 폭
                    int octaveWidth = (int)((float)scrollWidth/OCTAVE_COUNT); // 옥타브당 폭

                    int scrollX = view.getScrollX(); // 스크롤 위치
                    int bottom = view.getBottom()-scrollAreaBottom; // 건반 높이

                    float touchX = event.getX(downPointerIndex);
                    float touchY = event.getY(downPointerIndex)-scrollAreaBottom;
                    if(touchY<0) return false;

                    final int touchKeyX = scrollX + (int) touchX; // 이미지 상의 터치 X 좌표

                    int touchKeyPos = (touchKeyX / keyWhiteWidth); // 몇번째 흰 건반인가
                    int touchYPosPercent = (int)((touchY/((float)bottom))*100); // Y좌표는 height 대비  몇 % 지점에 찍혔는가

                    divideNote(touchKeyPos);
                    //옥타브 계산
                    int octave = (touchKeyX/octaveWidth)+1;

                    String key = ""+KEYS.charAt(touchKeyPos % (KEY_LENGTH));
                    if(touchYPosPercent<55){
                        //전체 높이의 55% 이내에 찍혔으면, 검은 건반을 눌렀을 가능성이 있음.
                        //각 흰 건반의 경계로부터 30% 이내에 맞았을 경우, 건반의 경계를 파악하여, 그 자리에 검은 건반이 있는지 확인한다.
                        int nearLineX1 = ((touchKeyX/keyWhiteWidth)*keyWhiteWidth);
                        int nearLineX2 = (((touchKeyX/keyWhiteWidth)+1)*keyWhiteWidth);
                        if((touchKeyX-nearLineX1)<(nearLineX2-touchKeyX)){
                            //아랫쪽 건반에 가까울 경우
                            if(((touchKeyX-nearLineX1)/(float)keyWhiteWidth)<0.3f){
                                //검은 건반 유효(flat)
                                if("cf".indexOf(key)<0){
                                    int keyCharPos = KEYS.indexOf(key)-1;
                                    if(keyCharPos<0) keyCharPos = KEY_LENGTH;
                                    key = ""+KEYS.charAt(keyCharPos);
                                    key += "s";
                                }
                            }
                        }else{
                            //윗쪽 건반에 가까울 경우
                            if(((nearLineX2-touchKeyX)/(float)keyWhiteWidth)<0.3f){
                                //검은 건반 유효(sharp)
                                if("eb".indexOf(key)<0) key += "s";
                            }
                        }
                    }
                    key += octave;

                    int soundKey = sMap.get(key);
                    int streamVolume = mAudioManager.getStreamVolume(AudioManager.STREAM_MUSIC);
                    sPool.play(soundKey, streamVolume, streamVolume, 0, 0, 1);
                    voice=pre_voice;

                    //alert에 사진넣기위해서
                    LayoutInflater factory = LayoutInflater.from(SearchActivity.this);
                    final View v = factory.inflate(R.layout.dial_main,null);

                    ImageView i = (ImageView)v.findViewById(R.id.img);
                    i.setImageResource(R.drawable.mic);


                    //voice = pre_voice;
                    ad = new AlertDialog.Builder(SearchActivity.this);
                    ad.setTitle("말하세요!");
                    ad.setView(v);
                    ad.setPositiveButton("확인",new DialogInterface.OnClickListener(){
                        public void onClick(DialogInterface dialog, int id){
                            //after_voice=pre_voice;
                            //voice = pre_voice;
                            R_change(touchKeyX);
                            //voice = pre_voice;
                        }
                    });

                    TimerTask mTask;
                    Timer mTimer;
                    mTask = new TimerTask() {
                        @Override
                        public void run() {
                            ad.show();
                        }
                    };
                    mTimer = new Timer();
                    mTimer.schedule(mTask,5000);


                    //voice = pre_voice;
                }

                //터치 영역이 스크롤 영역인지 확인
                float touchY = event.getY();
                if(touchY>scrollAreaBottom)
                    return true;
                return false;
            }
        };

        private View.OnTouchListener keysContainerTouchListener = new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                return false;
            }
        };

        @Override
        public boolean onKeyDown(int keyCode, KeyEvent event) {
            switch (keyCode) {
                case KeyEvent.KEYCODE_VOLUME_DOWN:
                    mAudioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_RAISE, AudioManager.FLAG_SHOW_UI);
                    return true;
                case KeyEvent.KEYCODE_VOLUME_UP:
                    mAudioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_LOWER, AudioManager.FLAG_SHOW_UI);
                    return true;
            }

            return super.onKeyDown(keyCode, event);
        }

        public void divideNote(int n){
            di_top = n/7;
            di_bottom=n%7;

            pre = (float)(notes.get(di_bottom) *Math.pow(2,di_top));
        }

        public void R_change(int change_n){
            after_voice=pre_voice;
            float gap = (float)(10*Math.pow(2,di_top-1));
            Toast.makeText(getApplicationContext(),"보이스"+voice+"피아노:"+pre+" 음정:"+after_voice,Toast.LENGTH_SHORT).show();
            if(after_voice!=voice&&after_voice>=pre-gap&&after_voice<=pre+gap){
                if(r_left==0 && r_right==0){
                    r_left = change_n;
                    r1.getLayoutParams().width = r_left;
                    r2.getLayoutParams().width = 1;
                }
                else if(r_right==0){
                    if(change_n>r_left)
                        r_right = change_n;
                    else{
                        r_right = r_left;
                        r_left = change_n;
                    }
                    r1.getLayoutParams().width = r_left;
                    r2.getLayoutParams().width = r_right-r_left;
                }
                else{
                    if(change_n<r_left)
                        r_left = change_n;
                    else if(change_n>r_right)
                        r_right = change_n;
                    r1.getLayoutParams().width = r_left;
                    r2.getLayoutParams().width = r_right-r_left;
                }
                Toast.makeText(getApplicationContext(),"피아노:"+pre+" 음정:"+after_voice,Toast.LENGTH_SHORT).show();
           }
           if(after_voice==voice){
                Toast.makeText(getApplicationContext(),"음을 말하세요!!!",Toast.LENGTH_SHORT).show();
           }

        }

        /**
         * Sound Pool을 재설정합니다.
         */
        private void resetSoundPool(){

            Map<String, Integer> tmpMap = new HashMap<String, Integer>();
            SoundPool tmpPool = new SoundPool(3, AudioManager.STREAM_MUSIC, 0);

            //미디 파일 생성
            try {
                programNo = pref.getInt("programNo", 1);
                octaveShift = pref.getInt("octaveShift", 0);
                MidiFileCreator midiFileCreator = new MidiFileCreator(SearchActivity.this);
                midiFileCreator.createMidiFiles(programNo, octaveShift);
            } catch (IOException e) {
                e.printStackTrace();
            }

            String dir = getDir("", MODE_PRIVATE).getAbsolutePath();
            for(int i=1;i<=OCTAVE_COUNT;i++){
                for (int j=0;j<PITCHES.length;j++){
                    String soundPath = dir+ File.separator+PITCHES[j]+i+".mid";
                    tmpMap.put(PITCHES[j]+i, tmpPool.load(soundPath, 1));
                }
            }

            sMap = tmpMap;
            sPool = tmpPool;
        }

        @Override
        protected void onStop() {
            // 현재 스크롤 상태를 저장합니다.
            SharedPreferences.Editor editor = pref.edit();
            editor.putInt("viewKeysScrollX", viewKeys.getScrollX());
            editor.commit();
            super.onStop();
        }

    @Override
    public void onBackPressed(){
        finish();
    }
}
