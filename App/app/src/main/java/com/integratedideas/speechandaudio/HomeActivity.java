package com.integratedideas.speechandaudio;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class HomeActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        Button b1 = (Button)findViewById(R.id.b1);
        Button b2 = (Button)findViewById(R.id.b2);
        Button b3 = (Button)findViewById(R.id.b3);
        Button b4 = (Button)findViewById(R.id.b4);

        b1.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
            }
        });

    }

    @Override
    public void onBackPressed(){
        finish();
    }
}
