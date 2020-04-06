package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Dialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;

import com.example.adeb.InterNet.Api_Calling;
import com.example.adeb.InterNet.MySharedPrefrence;
import com.example.adeb.InterNet.URLS;
import com.example.adeb.InterNet.onResult;
import com.example.adeb.R;
import com.example.adeb.Utility.Comman;
import com.example.adeb.Utility.Constant;
import com.example.adeb.Widget.Segow_UI_EditText;
import com.example.adeb.Widget.Segow_UI_Font;
import com.example.adeb.Widget.otpEditText;
import com.victor.loading.rotate.RotateLoading;

import org.json.JSONException;
import org.json.JSONObject;

public class ChangePassword_Activity extends AppCompatActivity implements onResult {
    Segow_UI_Font your_email;
    Segow_UI_EditText new_password;

    RelativeLayout relativeLayout;
    com.example.adeb.InterNet.onResult onResult;
    Dialog dialog;
    String Email;
    MySharedPrefrence m;
    private RotateLoading rotateLoading;

    Button Reset_password,login;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password_);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        m= MySharedPrefrence.instanceOf(getApplicationContext());
        this.onResult=this;

        //Having otp
        Intent i=getIntent();
        if(i!=null)
            Email=i.getStringExtra("email");


        your_email=findViewById(R.id.your_email);
        your_email.setText(m.getUserEmail());
        new_password=findViewById(R.id.new_password);
        Reset_password=findViewById(R.id.reset_password);
        relativeLayout = findViewById(R.id.progress);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);

        Reset_password.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!new_password.getText().toString().isEmpty()) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(ChangePassword_Activity.this, getWindow().getDecorView().getRootView(), onResult, URLS.UPDATE_PASSWORD, setPasswordChangeJson(), "otp_change");

                } else {
                    Comman.topSnakBar(ChangePassword_Activity.this, v, Constant.PLEASE_FILL_THIS_FIELD);
                }
            }
        });
    }

    private JSONObject setPasswordChangeJson() {

        JSONObject jsonObject=new JSONObject();
        try {
            jsonObject.put("email",""+Email).put("password",""+new_password.getText().toString());
            Comman.log("EmailFromMySide",""+jsonObject);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return  jsonObject;
    }

    @Override
    public void onResult(JSONObject jsonObject, Boolean status) {
        relativeLayout.setVisibility(View.GONE);
        rotateLoading.stop();
        if (status){
            dialog = new Dialog(ChangePassword_Activity.this);
            dialog.setContentView(R.layout.password_change_dailog);
            dialog.getWindow().addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP |Intent.FLAG_ACTIVITY_NEW_TASK );
            dialog.setCanceledOnTouchOutside(false);
            int Width =(int) (getResources().getDisplayMetrics().widthPixels*0.95);
            int Height =(int) (getResources().getDisplayMetrics().heightPixels*0.70);
            dialog.show();
            dialog.getWindow().setLayout(Width,Height);
            login=dialog.findViewById(R.id.buttonOk);
            login.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    startActivity(new Intent(ChangePassword_Activity.this,LoginActivity.class));
                }
            });
        }
    }
}
