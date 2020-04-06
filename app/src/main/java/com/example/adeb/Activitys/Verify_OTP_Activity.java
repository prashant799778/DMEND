package com.example.adeb.Activitys;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
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

public class Verify_OTP_Activity extends AppCompatActivity implements onResult {

    otpEditText otpEdit;
    Segow_UI_Font mobile_no;
    RelativeLayout relativeLayout;
    private RotateLoading rotateLoading;
    Dialog dialog;

    Button done,login;
    Context context;
    onResult onResult;
    ProgressBar progressBar;
    MySharedPrefrence m;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify__otp);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        m= MySharedPrefrence.instanceOf(getApplicationContext());
        //otpEditText
        otpEdit=findViewById(R.id.verify_otp);
        mobile_no=findViewById(R.id.mobile_no);
        mobile_no.setText(m.getMobile());
        this.onResult=this;
        //VerifyButton Click
        done=findViewById(R.id.Verify);
        rotateLoading = (RotateLoading) findViewById(R.id.rotateloading);
        relativeLayout=findViewById(R.id.progress);

        done.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (!otpEdit.getText().toString().isEmpty() ) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    rotateLoading.start();
                    Api_Calling.postMethodCall(Verify_OTP_Activity.this, getWindow().getDecorView().getRootView(), onResult, URLS.VERIFY, setStartJson(), "VerifyOTP");
                }else {
                    Comman.topSnakBar(context,v, Constant.PLEASE_FILL_ALL_FIELD);

                }
//                Rect displayRectangle = new Rect();
//                Window window = Verify_OTP_Activity.this.getWindow();
//                window.getDecorView().getWindowVisibleDisplayFrame(displayRectangle);
//                final MaterialAlertDialogBuilder alertDialogBuilder=new MaterialAlertDialogBuilder(Verify_OTP_Activity.this,R.style.custom_dialog);
//                final AlertDialog alertDialog = alertDialogBuilder.create();
//                alertDialogBuilder.setMessage(getResources().getString(R.string.verifyText2));
//                final View dialogView = LayoutInflater.from(v.getContext()).inflate(R.layout.otp_dialog_box, null, false);
//
//                Button ok=dialogView.findViewById(R.id.buttonOk);
//                alertDialog.setView(dialogView);
//                alertDialog.show();
//                ok.setOnClickListener(new View.OnClickListener() {
//                    @Override
//                    public void onClick(View v) {
//
//
//                        alertDialog.dismiss();
//                    }
//                });
            }
        });

        String otp= getIntent().getExtras().getString("otp");
        if(otp != null)
//            otpEditText.setText(otp.toString().trim());
            otpEdit.setText(otp.trim());
    }

    private JSONObject setStartJson()
    { String mobile = getIntent().getStringExtra("mobileNo");
        JSONObject jsonObject=new JSONObject();
        try {
            jsonObject.put("otp",""+otpEdit.getText().toString())
                      .put("mobileNo",mobile)
                      .put("deviceKey",""+m.getDeviceID());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return jsonObject;


    }





    @Override
    public void onResult(JSONObject jsonObject, Boolean status) {

       relativeLayout.setVisibility(View.GONE);
        if(jsonObject!=null && status) {
            JSONObject result=null;

            try {
                result= jsonObject.getJSONObject("result");
                Comman.log("Verify",""+result.toString());
                m.setMobile(Comman.getValueFromJsonObject(result,"mobileNo"));
                m.setotp(Comman.getValueFromJsonObject(result,"otp"));
                m.setUserId(Comman.getValueFromJsonObject(result,"userId"));
                m.setUserTypeId(Comman.getValueFromJsonObject(result,"userTypeId"));

                dialog = new Dialog(Verify_OTP_Activity.this);
                dialog.setContentView(R.layout.otp_dialog_box);
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
                         startActivity(new Intent(Verify_OTP_Activity.this,LoginActivity.class));
                     }
                 });
            } catch (JSONException e) {
                e.printStackTrace();
            }


        }

    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        relativeLayout.setVisibility(View.GONE);
    }
}
