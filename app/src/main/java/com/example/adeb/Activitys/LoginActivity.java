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
import android.widget.TextView;

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

public class LoginActivity extends AppCompatActivity implements View.OnClickListener, onResult {
    EditText phone, password;
    InputType inputType;
    Segow_UI_Font signUp, forgot;
    Segow_UI_EditText UserMobile, UserPassword;
    RelativeLayout relativeLayout;
    onResult onResult;
    Dialog dialog;
    MySharedPrefrence m;
    private RotateLoading rotateLoading;

    Button login;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        m= MySharedPrefrence.instanceOf(getApplicationContext());
        this.onResult=this;
        phone = findViewById(R.id.phone);
        password = findViewById(R.id.pswd);
        signUp = findViewById(R.id.signUp);
        forgot = findViewById(R.id.forgot);
        login = findViewById(R.id.login);
        UserMobile = findViewById(R.id.phone);
        UserPassword = findViewById(R.id.pswd);
        relativeLayout = findViewById(R.id.progress);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);
        login.setOnClickListener(this);
        signUp.setOnClickListener(this);
        forgot.setOnClickListener(this);


    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.signUp:
                startActivity(new Intent(LoginActivity.this, SignUPActivity.class));
                break;
            case R.id.forgot:
                startActivity(new Intent(LoginActivity.this, ForgotPasswordActivity.class));
                break;
            case R.id.login:

                if (!UserMobile.getText().toString().isEmpty() && !UserPassword.getText().toString().isEmpty()) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(LoginActivity.this, getWindow().getDecorView().getRootView(), onResult, URLS.LOGIN, setLoginJson(), "Login");

                } else {
                    Comman.topSnakBar(LoginActivity.this, v, Constant.PLEASE_FILL_ALL_FIELD);
                }
                break;
        }
    }

    private JSONObject setLoginJson() {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("mobileNo", "" + UserMobile.getText().toString())
                    .put("password", "" + UserPassword.getText().toString());

        } catch (JSONException e) {
            e.printStackTrace();
        }
        return jsonObject;
    }

    @Override
    public void onResult(JSONObject jsonObject, Boolean status) {

        relativeLayout.setVisibility(View.GONE);
        rotateLoading.stop();
        if (jsonObject !=null && status){
            m.setLoggedIn(true);
            Comman.log("Login","value"+jsonObject.toString());
            m.setMobile(Comman.getValueFromJsonObject(jsonObject,"mobileNo"));
            m.setUserId(Comman.getValueFromJsonObject(jsonObject,"userId"));
            m.setUserTypeId(Comman.getValueFromJsonObject(jsonObject,"userTypeId"));
            m.setUserName(Comman.getValueFromJsonObject(jsonObject,"name"));
            Intent i = new Intent(LoginActivity.this, BottomTabDashBoardActivity.class);
            i.putExtra("name", "" + Comman.getValueFromJsonObject(jsonObject, "name"));
            startActivity(i);
        }

    }
}
