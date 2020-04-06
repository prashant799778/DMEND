package com.example.adeb.InterNet;

import android.content.Context;
import android.view.View;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.error.VolleyError;
import com.android.volley.request.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.adeb.Utility.Comman;
import com.example.adeb.Utility.Constant;

import org.json.JSONException;
import org.json.JSONObject;

public class Api_Calling {

    public static void getMethodCall(final Context context, String URL, final View view, final onResult onResult, final String name)
    {
        if(!Comman.isConnectedToInternet(context))
        {
            Comman.topSnakBar(context,view, Constant.NO_INTERNET);
            onResult.onResult(null,false);
        }else {
            final JsonObjectRequest jsonObjectRequest=new JsonObjectRequest(Request.Method.GET, URL, null, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    Comman.log(name,""+response);
                    try {
                        if(Boolean.parseBoolean(response.getString("status"))){
                            onResult.onResult(response,true);}else {
                            onResult.onResult(response,false);
                            Comman.topSnakBar(context,view, response.getString("message"));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                        Comman.topSnakBar(context,view, Constant.SOMETHING_WENT_WRONG);
                    }
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {

                }
            });
            final RequestQueue requestQueue= Volley.newRequestQueue(context);
            requestQueue.add(jsonObjectRequest);
            requestQueue.addRequestFinishedListener(new RequestQueue.RequestFinishedListener<Object>() {
                @Override
                public void onRequestFinished(Request<Object> request) {
                    requestQueue.getCache().clear();
                }
            });
        }

    }
    public static void postMethodCall(final Context context, final View view, final onResult onResult, String URL, JSONObject jsonObject, final String name)
    {
        if(!Comman.isConnectedToInternet(context))
        {
            Comman.topSnakBar(context,view, Constant.NO_INTERNET);
            onResult.onResult(null,false);
        }else {
            JsonObjectRequest jsonObjectRequest=new JsonObjectRequest(Request.Method.POST, URL, jsonObject, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    Comman.log(name,"yyyyy"+response);
                    try {
                        if(Boolean.parseBoolean(response.getString("status"))){
                            onResult.onResult(response,true);}else {
                            onResult.onResult(null,false);
                            Comman.topSnakBar(context,view, response.getString("message"));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                        Comman.topSnakBar(context,view, Constant.SOMETHING_WENT_WRONG);
                    }
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {

                }
            });
            RequestQueue requestQueue=Volley.newRequestQueue(context);
            requestQueue.add(jsonObjectRequest);

        }

    }
}
