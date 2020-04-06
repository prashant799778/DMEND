package com.example.adeb.Fragments;

import android.Manifest;
import android.animation.Animator;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.drawable.Drawable;
import android.icu.text.Transliterator;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.Placeholder;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.Toast;

import com.example.adeb.R;
import com.example.adeb.Widget.Segow_UI_EditText;
import com.example.adeb.Widget.Segow_UI_Font;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptor;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;

import java.io.IOException;
import java.util.List;
import java.util.Locale;

public class BookDriverFragment extends Fragment implements View.OnClickListener, OnMapReadyCallback, LocationListener {

    LinearLayout lay_DayDriver, lay_Corporate, lay_Hourly, lay_OneRound;
    Segow_UI_Font day_driver, corporate, hourly, one_round;
    private GoogleMap mMap;
    ImageView cross, cross2, close_layout, game, close_game, logo_game;
    Segow_UI_EditText pickup_address, destination_address;
    ImageView expand;
    ValueAnimator mAnimator;
    public double latitude;
    public double longitude;
    LatLng latLng;
    Animation myAnim, mylogo, myclose, bounce;

    RelativeLayout relativeLayout, relativeLayout2, game_Layout;

    FusedLocationProviderClient fusedLocationProviderClient;
    Location currentLocation;
    Placeholder placeholder;
    Marker marker;
    Location mlocation;
    Transliterator.Position myPosition;
    double v;
    private static final int REQUEST_CODE = 101;


    public BookDriverFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_book_driver, container, false);

        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(getContext());
        fetchLocation();


        ////////////LoGo//////////
        game = rootView.findViewById(R.id.game);
        game_Layout = rootView.findViewById(R.id.game_layout);
        close_game = rootView.findViewById(R.id.close_game_layout);
        logo_game = rootView.findViewById(R.id.logo_game_layout);
        myclose = AnimationUtils.loadAnimation(getContext(), R.anim.slide_down);
        myAnim = AnimationUtils.loadAnimation(getContext(), R.anim.slide_up);
        mylogo = AnimationUtils.loadAnimation(getContext(), R.anim.sequicial);
        bounce = AnimationUtils.loadAnimation(getContext(), R.anim.bounce);
        logo_game.setAnimation(bounce);
        logo_game.setAnimation(mylogo);


        expand = rootView.findViewById(R.id.expand);
        close_layout = rootView.findViewById(R.id.close_layout);
        relativeLayout = rootView.findViewById(R.id.layout1);
        relativeLayout2 = rootView.findViewById(R.id.layout2);


        //EditText
        pickup_address = rootView.findViewById(R.id.pickUpAdress);
        destination_address = rootView.findViewById(R.id.distination_address);

        //Cross ImageView
        cross2 = rootView.findViewById(R.id.cross2);
        cross = rootView.findViewById(R.id.cross);

        //Layouts//
        lay_DayDriver = rootView.findViewById(R.id.lay_day_driver);
        lay_Corporate = rootView.findViewById(R.id.lay_corporate);
        lay_Hourly = rootView.findViewById(R.id.lay_hourly);
        lay_OneRound = rootView.findViewById(R.id.lay_one_round);

        //TextView//
        day_driver = rootView.findViewById(R.id.day_driver);
        corporate = rootView.findViewById(R.id.corporate);
        hourly = rootView.findViewById(R.id.hourly);
        one_round = rootView.findViewById(R.id.oneRound);

        //onclick
        day_driver.setOnClickListener(this);
        corporate.setOnClickListener(this);
        hourly.setOnClickListener(this);
        one_round.setOnClickListener(this);
        cross.setOnClickListener(this);
        expand.setOnClickListener(this);
        cross2.setOnClickListener(this);
        close_layout.setOnClickListener(this);
        game.setOnClickListener(this);
        close_game.setOnClickListener(this);
        logo_game.setOnClickListener(this);

        //Visibility
        day_driver.setVisibility(View.VISIBLE);
        corporate.setVisibility(View.VISIBLE);
        hourly.setVisibility(View.VISIBLE);
        one_round.setVisibility(View.VISIBLE);
        cross.setVisibility(View.GONE);
        cross2.setVisibility(View.GONE);
        relativeLayout.setVisibility(View.VISIBLE);

        ///////////////////// Map work to set current Location//////////////////////////////////////



        //PickUp Address EditText
        pickup_address.addTextChangedListener(new TextWatcher() {
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
        // Destination Address EditText
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

        //////////////// Handling Car and Gear type layout//////////////////////////
        relativeLayout2.getViewTreeObserver().addOnPreDrawListener(new ViewTreeObserver.OnPreDrawListener() {
            @Override
            public boolean onPreDraw() {
                relativeLayout2.getViewTreeObserver().removeOnPreDrawListener(this);
                relativeLayout2.setVisibility(View.GONE);

                final int widthSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
                final int heightSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
                relativeLayout2.measure(widthSpec, heightSpec);
                mAnimator = slideAnimator(0, relativeLayout2.getMeasuredHeight());
                return true;
            }
        });


        return rootView;
    }


    private ValueAnimator slideAnimator(int i, int measuredHeight) {

        ValueAnimator animator = ValueAnimator.ofInt(i, measuredHeight);


        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator valueAnimator) {
                //Update Height
                int value = (Integer) valueAnimator.getAnimatedValue();

                ViewGroup.LayoutParams layoutParams = relativeLayout2.getLayoutParams();
                layoutParams.height = value;
                relativeLayout2.setLayoutParams(layoutParams);
            }
        });
        return animator;
    }

    private void collapse() {
        int finalHeight = relativeLayout.getHeight();

        ValueAnimator mAnimator = slideAnimator(finalHeight, 0);

        mAnimator.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationEnd(Animator animator) {
                //Height=0, but it set visibility to GONE
                relativeLayout2.setVisibility(View.GONE);
            }

            @Override
            public void onAnimationStart(Animator animator) {
                relativeLayout.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationCancel(Animator animator) {
            }

            @Override
            public void onAnimationRepeat(Animator animator) {
            }
        });
        mAnimator.start();
    }

    private void expand() {

        relativeLayout2.setVisibility(View.VISIBLE);
        mAnimator.start();
    }

    @Override
    public void onClick(View v) {

        switch (v.getId()) {

            /////////////Option Select////////////
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

            ///////////////To Clear Present Text In EditText////////////////
            case R.id.cross:
                pickup_address.getText().clear();
                break;

            case R.id.cross2:
                destination_address.getText().clear();
                break;
            ////////////////Car and Gear type layout/////////////////////
            case R.id.expand:
                if (relativeLayout2.getVisibility() == View.GONE) {
                    relativeLayout.setVisibility(View.VISIBLE);
                    expand.setVisibility(View.GONE);
                    close_layout.setVisibility(View.VISIBLE);
                    expand();
                } else {
                    collapse();
                    expand.setVisibility(View.VISIBLE);
                    close_layout.setVisibility(View.GONE);
                }
                break;
            case R.id.close_layout:
                collapse();
                expand.setVisibility(View.VISIBLE);
                close_layout.setVisibility(View.GONE);
                break;
//////////////////////////////////logo Animation/////////////////////////////
            case R.id.game:
                game_Layout.setVisibility(View.VISIBLE);
                close_game.setVisibility(View.VISIBLE);
                break;

            case R.id.close_game_layout:
                game_Layout.setVisibility(View.GONE);

                break;
            case R.id.logo_game_layout:
                if (mylogo == mylogo) {
                    v.startAnimation(bounce);

                }

                break;
        }


    }

    /////////////////////Map Work//////////////////////////
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        mMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        mMap.getUiSettings().setRotateGesturesEnabled(true);
        mMap.setTrafficEnabled(true);
        mMap.setMyLocationEnabled(true);

        if (currentLocation != null) {
            double latitude = currentLocation.getLatitude();
            double longitude = currentLocation.getLongitude();
            latLng = new LatLng(latitude, longitude);
            mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));
            mMap.animateCamera(CameraUpdateFactory.zoomTo(15));
            mMap.addMarker(new MarkerOptions()
                    .position(latLng)
                    .icon(bitmapDescriptorFromVector(getActivity(), R.drawable.ic_pin))
                    .title("title"));
            CameraPosition cameraPosition = new CameraPosition.Builder()
                    .target(latLng)      // Sets the center of the map to Mountain View
                    .zoom(mMap.getCameraPosition().zoom)
                    .bearing(currentLocation.getBearing())                // Sets the orientation of the camera to east// Sets the zoom
                    .tilt(90)
                    .zoom(13.f)// Sets the tilt of the camera to 30 degrees
                    .build();                   // Creates a CameraPosition from the builder
            mMap.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition));

            Log.d("Address","asxascasc");
            LatLng latLng= new LatLng(currentLocation.getLatitude(),currentLocation.getLongitude());
            Geocoder geocoder = new Geocoder(getContext(), Locale.getDefault());
            List<Address> addresses = null;
            try {
                addresses = geocoder.getFromLocation(currentLocation.getLatitude(), currentLocation.getLongitude(), 1);
                String cityName = addresses.get(0).getAddressLine(0);
                String stateName = addresses.get(0).getAddressLine(1);
                pickup_address.setText(cityName + ", " + stateName);
            } catch (IOException e) {
                e.printStackTrace();
            }

        }


    }

    private void fetchLocation() {
        if (ActivityCompat.checkSelfPermission(
                getContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                getContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions((Activity) getContext(), new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, REQUEST_CODE);
            return;
        }
        Task<Location> task = fusedLocationProviderClient.getLastLocation();
        task.addOnSuccessListener(new OnSuccessListener<Location>() {
            @Override
            public void onSuccess(Location location) {
                if (location != null) {
                    currentLocation = location;
                    Toast.makeText(getContext(), currentLocation.getLatitude() + "" + currentLocation.getLongitude(), Toast.LENGTH_LONG).show();
                    fragMap();
                }
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode) {
            case REQUEST_CODE:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    fetchLocation();
                }
                break;
        }
    }

    @Override
    public void onLocationChanged(Location location) {


    }

    public void fragMap(){
        SupportMapFragment mapFragment = (SupportMapFragment) getChildFragmentManager().findFragmentById(R.id.map_fargment);
        assert mapFragment != null;
        mapFragment.getMapAsync(this);
    }

    private BitmapDescriptor bitmapDescriptorFromVector(Context context, int vectorResId) {
        Drawable vectorDrawable = ContextCompat.getDrawable(context, vectorResId);
        vectorDrawable.setBounds(0, 0, vectorDrawable.getIntrinsicWidth(), vectorDrawable.getIntrinsicHeight());
        Bitmap bitmap = Bitmap.createBitmap(vectorDrawable.getIntrinsicWidth(), vectorDrawable.getIntrinsicHeight(), Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        vectorDrawable.draw(canvas);
        return BitmapDescriptorFactory.fromBitmap(bitmap);
    }
}