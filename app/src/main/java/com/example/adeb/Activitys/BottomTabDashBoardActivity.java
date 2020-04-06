package com.example.adeb.Activitys;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import com.example.adeb.Adpters.BottomTabViewPagerAdapter;
import com.example.adeb.Fragments.BookDriverFragment;
import com.example.adeb.Fragments.PaymentMethodFragment;
import com.example.adeb.Fragments.ProfileFragments;
import com.example.adeb.Fragments.YourBookingFragment;
import com.example.adeb.R;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class BottomTabDashBoardActivity extends AppCompatActivity {

    BottomNavigationView bottomNavigationView;
    private ViewPager viewPager;

    //Fragments
    YourBookingFragment yourBookingFragment;
    ProfileFragments profileFragments;
    PaymentMethodFragment paymentMethodFragment;
    BookDriverFragment bookDriverFragment;

    MenuItem menuItem;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bottom_tab_dash_board);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        //Initializing viewPager
        viewPager = (ViewPager) findViewById(R.id.view_pager);

        //Initializing the bottomNavigationView
        bottomNavigationView = (BottomNavigationView) findViewById(R.id.bottom_tab_view);

        bottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.book_driver:
                        viewPager.setCurrentItem(0);
                        break;
                    case R.id.my_bookings:
                        viewPager.setCurrentItem(1);
                        break;
                    case R.id.payment_methods:
                        viewPager.setCurrentItem(2);
                        break;
                    case R.id.profile:
                        viewPager.setCurrentItem(3);
                        break;
                }
                return false;
            }
        });

        viewPager.addOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {

            }

            @Override
            public void onPageSelected(int position) {
                if (menuItem != null) {
                    menuItem.setChecked(false);
                } else {
                    bottomNavigationView.getMenu().getItem(0).setChecked(false);
                }
                Log.d("page", "onPageSelected: " + position);
                bottomNavigationView.getMenu().getItem(position).setChecked(true);
                menuItem = bottomNavigationView.getMenu().getItem(position);

            }

            @Override
            public void onPageScrollStateChanged(int state) {

            }
        });

        setupViewPager(viewPager);
    }

    private void setupViewPager(ViewPager viewPager) {
        BottomTabViewPagerAdapter adapter = new BottomTabViewPagerAdapter(getSupportFragmentManager());
        yourBookingFragment=new YourBookingFragment();
        paymentMethodFragment =new PaymentMethodFragment();
        bookDriverFragment=new BookDriverFragment();
        profileFragments=new ProfileFragments();
        adapter.addFragment(bookDriverFragment);
        adapter.addFragment(yourBookingFragment);
        adapter.addFragment(paymentMethodFragment);
        adapter.addFragment(profileFragments);
        viewPager.setAdapter(adapter);
    }

    private boolean doubleBackToExitPressedOnce = false;
    @Override
    protected void onResume() {
        super.onResume();
        this.doubleBackToExitPressedOnce = false;
    }
    @Override
    public void onBackPressed() {

        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            return;
        }
        this.doubleBackToExitPressedOnce = true;

        Intent a = new Intent(Intent.ACTION_MAIN);
        a.addCategory(Intent.CATEGORY_HOME);
        a.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(a);
    }
}
