package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Dialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
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
import com.victor.loading.rotate.RotateLoading;

import org.json.JSONException;
import org.json.JSONObject;

public class ForgotPasswordActivity extends AppCompatActivity implements onResult {
    InputType inputType;
    Segow_UI_Font signUp, forgot;
    Segow_UI_EditText UserEmail;
    RelativeLayout relativeLayout;
    onResult onResult;
    Dialog dialog;
    MySharedPrefrence m;
    private RotateLoading rotateLoading;

    Button Continue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_forgot_password);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        m= MySharedPrefrence.instanceOf(getApplicationContext());
        this.onResult=this;
        Continue=findViewById(R.id.Continue);
        relativeLayout = findViewById(R.id.progress);
        UserEmail=findViewById(R.id.ed_email);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);
        Continue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!UserEmail.getText().toString().isEmpty()) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(ForgotPasswordActivity.this, getWindow().getDecorView().getRootView(), onResult, URLS.GET_OTP, setForGotJson(), "otp");

                } else {
                    Comman.topSnakBar(ForgotPasswordActivity.this, v, Constant.PLEASE_FILL_ALL_FIELD);
                }
            }
        });


    }

    private JSONObject setForGotJson() {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("email", "" + UserEmail.getText().toString());

        } catch (JSONException e) {
            e.printStackTrace();
        }
        return jsonObject;
    }

    @Override
    public void onResult(JSONObject jsonObject, Boolean status) {
        relativeLayout.setVisibility(View.GONE);
        rotateLoading.stop();
        String otp="";
        if(status) {
            Intent intent = new Intent(ForgotPasswordActivity.this, OTP_Activity.class);
            intent.putExtra("email", "" + UserEmail.getText().toString());
            intent.putExtra("otp", otp);
            startActivity(intent);
            m.setUserEmail(Comman.getValueFromJsonObject(jsonObject,"email"));
        }
    }
}
