package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Vibrator;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;

import com.example.adeb.R;
import com.example.adeb.Utility.Comman;

public class SplashScreen extends AppCompatActivity {
   private RelativeLayout relativeLayout;
   Handler handler;
    private Runnable callback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_screen);

        relativeLayout=findViewById(R.id.anim_splash);


        Animation animation = AnimationUtils.loadAnimation(this,R.anim.fade);
        relativeLayout.startAnimation(animation);

        handler = new Handler();
        callback = new Runnable() {
            @Override
            public void run() {
                if (Comman.Check_Login(SplashScreen.this)){
                        startActivity(new Intent(SplashScreen.this,BottomTabDashBoardActivity.class));

                    }else {
                        startActivity(new Intent(SplashScreen.this,LoginActivity.class));

                    }
                finish();
                overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            }
        };
        handler.postDelayed(callback, 3000);
    }

    @Override
    protected void onPause() {
        super.onPause();
        handler.removeCallbacks(callback);
    }



}
