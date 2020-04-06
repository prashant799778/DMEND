package com.example.adeb.Activitys;

import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentManager;

import android.app.Dialog;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import com.example.adeb.Adpters.Drawer_Adapter;
import com.example.adeb.Fragments.PaymentMethods;
import com.example.adeb.Fragments.YourBookingFragment;
import com.example.adeb.Models.DrawerModel;
import com.example.adeb.R;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

public class MainDashboardActivity extends FragmentActivity implements OnMapReadyCallback, View.OnClickListener {

    private GoogleMap mMap;


    ListView listView;
    DrawerLayout drawerLayout;
    ImageView openDrawer,cross,cross2;
    EditText pickUpAddrdess,destination_address;
    ActionBarDrawerToggle actionBarDrawerToggle;
    LinearLayout lay_DayDriver,lay_Corporate,lay_Hourly,lay_OneRound;
    TextView day_driver,corporate,hourly,one_round;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_dashboard);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        pickUpAddrdess=findViewById(R.id.pickUpAdress);
        destination_address=findViewById(R.id.distination_address);
        cross2=findViewById(R.id.cross2);
        cross=findViewById(R.id.cross);

        //Layouts//
        lay_DayDriver=findViewById(R.id.lay_day_driver);
        lay_Corporate=findViewById(R.id.lay_corporate);
        lay_Hourly=findViewById(R.id.lay_hourly);
        lay_OneRound=findViewById(R.id.lay_one_round);

        //TextView//
        day_driver=findViewById(R.id.day_driver);
        corporate=findViewById(R.id.corporate);
        hourly=findViewById(R.id.hourly);
        one_round=findViewById(R.id.oneRound);

        //onclick
        day_driver.setOnClickListener(this);
        corporate.setOnClickListener(this);
        hourly.setOnClickListener(this);
        one_round.setOnClickListener(this);

        //Visibility
        day_driver.setVisibility(View.VISIBLE);
        corporate.setVisibility(View.VISIBLE);
        hourly.setVisibility(View.VISIBLE);
        one_round.setVisibility(View.VISIBLE);

        cross.setVisibility(View.GONE);
        cross2.setVisibility(View.GONE);

        pickUpAddrdess.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                cross.setVisibility(View.VISIBLE);

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        destination_address.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                cross2.setVisibility(View.VISIBLE);
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        cross.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                pickUpAddrdess.getText().clear();
            }
        });

        cross2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                destination_address.getText().clear();
            }
        });
        openDrawer=findViewById(R.id.open_dawer);
        listView = findViewById(R.id.left_drawer);
        openDrawer.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                drawerLayout = findViewById(R.id.drawerlayut);
                // If navigation drawer is not open yet, open it else close it.
                drawerLayout.addDrawerListener(actionBarDrawerToggle);
                if (!drawerLayout.isDrawerOpen(GravityCompat.START))
                    drawerLayout.openDrawer(Gravity.LEFT);
                else drawerLayout.closeDrawer(Gravity.LEFT);
            }
        });
        DrawerModel[] drawerItem = new DrawerModel[6];
        drawerItem[0] = new DrawerModel(R.drawable.ic_taxi, "Book a Driver");
        drawerItem[1] = new DrawerModel(R.drawable.ic_your_ride, "Your Bookings");
        drawerItem[2] = new DrawerModel(R.drawable.ic_rate_card, "Payment Methods");
        drawerItem[3] = new DrawerModel(R.drawable.ic_star, "Rate our App");
        drawerItem[4] = new DrawerModel(R.drawable.ic_about, "About");
        drawerItem[5] = new DrawerModel(R.drawable.ic_support, "Help");

        Drawer_Adapter adapter = new Drawer_Adapter(this, R.layout.drawer_list_view, drawerItem);
        listView.setOnItemClickListener(new DrawerItemClickListener());
        listView.setAdapter(adapter);
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }

    @Override
    public void onClick(View v) {

        switch (v.getId()){

            case R.id.day_driver:
                lay_DayDriver.setVisibility(View.VISIBLE);
                corporate.setVisibility(View.VISIBLE);
                lay_Hourly.setVisibility(View.GONE);
                lay_Corporate.setVisibility(View.GONE);
                lay_OneRound.setVisibility(View.GONE);

                break;

            case R.id.corporate:
                lay_DayDriver.setVisibility(View.GONE);
                day_driver.setVisibility(View.VISIBLE);
                lay_Corporate.setVisibility(View.VISIBLE);
                lay_OneRound.setVisibility(View.GONE);
                lay_Hourly.setVisibility(View.GONE);
                break;

            case R.id.hourly:
                corporate.setVisibility(View.VISIBLE);
                lay_Corporate.setVisibility(View.GONE);
                lay_Hourly.setVisibility(View.VISIBLE);
                lay_DayDriver.setVisibility(View.GONE);
                lay_OneRound.setVisibility(View.GONE);

                break;

            case R.id.oneRound:
                lay_Hourly.setVisibility(View.GONE);
                lay_DayDriver.setVisibility(View.GONE);
                lay_Hourly.setVisibility(View.GONE);
                lay_Corporate.setVisibility(View.GONE);
                hourly.setVisibility(View.VISIBLE);
                lay_OneRound.setVisibility(View.VISIBLE);
                break;
        }


    }

    private class DrawerItemClickListener implements android.widget.AdapterView.OnItemClickListener {
        @Override
        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
            selectItem(position);

        }
    }

    private void selectItem(int position) {


        Fragment fragment = null;


        switch (position) {
            case 0:
                drawerLayout.closeDrawers();
                break;

            case 1:
                fragment = new YourBookingFragment();
                drawerLayout.closeDrawers();
                break;

            case 2:
                fragment = new PaymentMethods();
                drawerLayout.closeDrawers();
                break;
            case 3:
                startActivity(new Intent(MainDashboardActivity.this, FavoriteDriverActivity.class));
                drawerLayout.closeDrawers();
                drawerLayout.closeDrawers();
                break;
            case 4:
                startActivity(new Intent(MainDashboardActivity.this, AboutActivity.class));
                drawerLayout.closeDrawers();
                break;

            case 5:
                startActivity(new Intent(MainDashboardActivity.this, HelpActivity.class));
                drawerLayout.closeDrawers();
                break;


        }
        if (fragment != null) {
            FragmentManager fragmentManager = getSupportFragmentManager();
            fragmentManager.beginTransaction().replace(R.id.map, fragment).commit();
            listView.setItemChecked(position, true);
            listView.setSelection(position);

        } else {
            Log.e("MainActivity", "Error in creating fragment");
        }
    }


    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng sydney = new LatLng(-34, 151);
        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
    }
}
