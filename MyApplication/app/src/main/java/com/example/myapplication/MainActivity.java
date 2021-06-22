package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.ButtonBarLayout;

import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.ContextMenu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {
    Button btnOn,btnOff;
    EditText text;
    Socket mysocket = null;
    public static String wifiModuleIp="";
    public static int wifiModulePort=0;
    public static String CMD ="0";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnOn = (Button)findViewById(R.id.button);
        btnOff = (Button)findViewById(R.id.button2);
        text = (EditText) findViewById(R.id.texts);

        btnOn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getIPandPort();
                CMD="a";
                Soket_AsyncTask cmd_on = new Soket_AsyncTask();
                cmd_on.execute();
            }
        });
        btnOff.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getIPandPort();
                CMD="b";
                Soket_AsyncTask cmd_off = new Soket_AsyncTask();
                cmd_off.execute();
            }
        });
    }
    public void getIPandPort(){
        String ipandport=text.getText().toString();
        Log.d("MYTEST","IP String: "+ipandport);
        String temp[]=ipandport.split(":");
        wifiModuleIp=temp[0];
        wifiModulePort=Integer.valueOf(temp[1]);
        Log.d("MY TEST","IP: "+wifiModuleIp);
        Log.d("MY TEST","PORT: "+wifiModulePort);
    }

    public class Soket_AsyncTask extends AsyncTask<Void,Void,Void>
    {
        Socket socket;
        @Override
        protected Void doInBackground(Void... voids) {
           try{
               InetAddress inetAddress=InetAddress.getByName(MainActivity.wifiModuleIp);
               socket=new Socket(inetAddress,MainActivity.wifiModulePort);
               DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
               dataOutputStream.writeBytes(CMD);
               dataOutputStream.close();
               socket.close();
           }catch (UnknownHostException e){e.printStackTrace();}catch (IOException e){e.printStackTrace();}
           return null;
        }
    }
}