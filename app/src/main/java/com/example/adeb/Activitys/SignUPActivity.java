package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.example.adeb.InterNet.Api_Calling;
import com.example.adeb.InterNet.MySharedPrefrence;
import com.example.adeb.InterNet.URLS;
import com.example.adeb.InterNet.onResult;
import com.example.adeb.R;
import com.example.adeb.Utility.Comman;
import com.example.adeb.Utility.Constant;
import com.victor.loading.rotate.RotateLoading;

import org.json.JSONException;
import org.json.JSONObject;

public class SignUPActivity extends AppCompatActivity implements View.OnClickListener, onResult {
   TextView al_login,terms;
   EditText name,Mobile,email,password;
   CheckBox checkBox;
   Button signUp;
   RelativeLayout relativeLayout;
   onResult onResult;
    private RotateLoading rotateLoading;
    MySharedPrefrence m;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_u_p);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        al_login=findViewById(R.id.al_login);
        terms=findViewById(R.id.terms);
        signUp=findViewById(R.id.signUp_btt);
        signUp.setOnClickListener(this);
        al_login.setOnClickListener(this);
        terms.setOnClickListener(this);
        relativeLayout=findViewById(R.id.progress);

        //EditText//
        name=findViewById(R.id.name);
        Mobile=findViewById(R.id.phone);
        email=findViewById(R.id.email);
        password=findViewById(R.id.pswd);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);

        //checkbox//
        checkBox=findViewById(R.id.check_box);
        this.onResult=this;
        m= MySharedPrefrence.instanceOf(getApplicationContext());

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.al_login:
                onBackPressed();
              break;
            case R.id.terms:
                startActivity(new Intent(SignUPActivity.this,TermsConditionActivity.class));
             break;

            case R.id.signUp_btt:
                if (!name.getText().toString().isEmpty() && !Mobile.getText().toString().isEmpty() && !email.getText().toString().isEmpty() && !password.getText().toString().isEmpty() && checkBox.isChecked()){
//                    RelativeLayout layout =new RelativeLayout(SignUPActivity.this);
//                    progressBar = new ProgressBar(SignUPActivity.this,null,android.R.attr.progressBarStyleLarge);
//                    RelativeLayout.LayoutParams params = new RelativeLayout.LayoutParams(200,200);
//                    params.addRule(RelativeLayout.CENTER_IN_PARENT);
//                    layout.addView(progressBar,params);
//                    setContentView(layout);
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(SignUPActivity.this, getWindow().getDecorView().getRootView(), onResult, URLS.USERSINGUP, setSingnUpJson(), "SignUp");

                }else if (!checkBox.isChecked()){
                    Comman.topSnakBar(SignUPActivity.this, v, Constant.CheckBox);

                }else {
                    Comman.topSnakBar(SignUPActivity.this, v, Constant.PLEASE_FILL_ALL_FIELD);
                }
                break;
        }

    }

    private JSONObject setSingnUpJson() {
        JSONObject jsonObject = new JSONObject();
        int deviceId=12345;
        try {
            jsonObject.put("name", "" + name.getText().toString())
                    .put("mobileNo", "" + Mobile.getText().toString())
                    .put("email", "" + email.getText().toString())
                    .put("deviceKey",""+deviceId)
                    .put("password", "" + password.getText().toString());

        } catch (JSONException e) {
            e.printStackTrace();
        }
        Comman.log("SignIpJSon", "" + jsonObject);
        return jsonObject;
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        relativeLayout.setVisibility(View.GONE);
    }


    @Override
    public void onResult(JSONObject jsonObject, Boolean status) {

            relativeLayout.setVisibility(View.GONE);
         rotateLoading.stop();
       if (jsonObject !=null && status){
           try
           {
               String otp = "";
               JSONObject jsonObject1= jsonObject.getJSONObject("result");
               otp = jsonObject1.getString("otp");
               Intent verificationIntent = new Intent(SignUPActivity.this, Verify_OTP_Activity.class);
               verificationIntent.putExtra("otp", otp);
               verificationIntent.putExtra("mobileNo", Mobile.getText().toString());
               startActivity(verificationIntent);

               m.setMobile(Comman.getValueFromJsonObject(jsonObject1,"mobileNo"));
               m.setotp(Comman.getValueFromJsonObject(jsonObject1,"otp"));
               m.setUserId(Comman.getValueFromJsonObject(jsonObject1,"userId"));
               m.setDeviceID(Comman.getValueFromJsonObject(jsonObject1,"deviceKey"));
               m.setUserTypeId(Comman.getValueFromJsonObject(jsonObject1,"userTypeId"));
           }
           catch (Exception e) {
               e.printStackTrace();
           }


        }
    }
//    public void show() {
//        progressBar.setVisibility(View.VISIBLE);
//    }
//
//    public void hide() {
//        progressBar.setVisibility(View.INVISIBLE);
//    }
}
