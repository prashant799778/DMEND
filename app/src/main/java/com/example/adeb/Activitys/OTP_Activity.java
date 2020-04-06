package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Dialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.text.InputType;
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

public class OTP_Activity extends AppCompatActivity  implements onResult{
    
    Segow_UI_Font email;
    otpEditText otp;
    RelativeLayout relativeLayout;
    com.example.adeb.InterNet.onResult onResult;
    Dialog dialog;
    String Email;
    MySharedPrefrence m;
    private RotateLoading rotateLoading;

    Button Reset;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_otp);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        m= MySharedPrefrence.instanceOf(getApplicationContext());
        this.onResult=this;
        otp=findViewById(R.id.et_otp_new);
        //Having otp
        Intent i=getIntent();
        String otp2= getIntent().getExtras().getString("otp");
        if(i!=null)
            Email=i.getStringExtra("email");
        otp.setText(otp2.trim());



        email=findViewById(R.id.email_user2);
        email.setText(m.getUserEmail());
        Reset=findViewById(R.id.reset);
        relativeLayout = findViewById(R.id.progress);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);
        
        Reset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!otp.getText().toString().isEmpty()) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(OTP_Activity.this, getWindow().getDecorView().getRootView(), onResult, URLS.ENTER_OTP, setOTPJson(), "otp");

                } else {
                    Comman.topSnakBar(OTP_Activity.this, v, Constant.PLEASE_FILL_THIS_FIELD);
                }
            }
        });
    }

    private JSONObject setOTPJson() {
        JSONObject jsonObject=new JSONObject();
        try {
            jsonObject.put("email",""+Email).put("otp",""+otp.getText().toString());
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
        if(status){
            Intent intent=new Intent(OTP_Activity.this,ChangePassword_Activity.class);
            intent.putExtra("email",""+Email);
            startActivity(intent);
            m.setotp(Comman.getValueFromJsonObject(jsonObject,"otp"));
        }
    }
}
