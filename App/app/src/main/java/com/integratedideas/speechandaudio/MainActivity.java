
package com.integratedideas.speechandaudio;


import android.app.ActionBar;
import android.app.FragmentTransaction;
import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TabHost;


public class MainActivity extends TabActivity {

	ActionBar actionBar;
	private DBHelper dbHelper;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		final TabHost tabHost = getTabHost();

		tabHost.addTab(tabHost.newTabSpec("tab1")
		.setIndicator("list1")
		.setContent(new Intent(this,HomeActivity.class)));

		tabHost.addTab(tabHost.newTabSpec("tab2")
				.setIndicator("list2")
				.setContent(new Intent(this,SearchActivity.class)));

		tabHost.addTab(tabHost.newTabSpec("tab3")
				.setIndicator("list3")
				.setContent(new Intent(this,HomeActivity.class)));

		String etDBName = "testDB";
		dbHelper = new DBHelper( MainActivity.this, etDBName, null, 1); dbHelper.testDB();

	}

	ActionBar.TabListener listener= new ActionBar.TabListener() {
		@Override
		public void onTabSelected(ActionBar.Tab tab, FragmentTransaction fragmentTransaction) {
			int position = tab.getPosition();



			switch( position ){
				case 0: //가장 왼쪽 Tab 선택(Analog)
					//MainActivity가 보여 줄 View를
					//res폴더>>layout폴더>>layout_tab_0.xml 로 설정
					setContentView(R.layout.activity_main);
					break;
				case 1:

					setContentView(R.layout.activity_search);
					break;
				case 2: //세번째 Tab 선택(Calendar)
					//MainActivity가 보여 줄 View를
					//res폴더>>layout폴더>>layout_tab_2.xml 로 설정
					setContentView(R.layout.activity_home);
					break;
			}
		}

		@Override
		public void onTabUnselected(ActionBar.Tab tab, FragmentTransaction ft) {
			// TODO Auto-generated method stub
		}

		@Override
		public void onTabReselected(ActionBar.Tab tab, FragmentTransaction fragmentTransaction) {
		}
	};

	@Override
	public void onBackPressed(){
		finish();
	}
}



