package com.tapmo;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import java.util.List;

public class MyActivity extends Activity {

    TextView text, text2;
    ImageView deskBackground;
    Uri data;
    ProgressBar progressBar;
    Context context;
    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        context = this;

        text = (TextView) findViewById(R.id.text);
        text2 = (TextView) findViewById(R.id.text2);
        deskBackground = (ImageView) findViewById(R.id.desk_background);
        progressBar = (ProgressBar) findViewById(R.id.progress_circle);

        data = getIntent().getData();

        if(data != null) {
            List<String> params = data.getPathSegments();
            String first = params.get(1);
            String second = params.get(3);

            text2.setVisibility(View.GONE);
            text.setVisibility(View.GONE);
            progressBar.setVisibility(View.VISIBLE);


            text.setText("User: " + first + "\tLocation: "+ second +"\t\tData: " + data.toString());

            AsyncHttpClient client = new AsyncHttpClient();
            client.post(data.toString(), new AsyncHttpResponseHandler() {
                @Override
                public void onSuccess(String response) {
                    int status = Integer.parseInt(response);
                    if(status == 1) {
                        deskBackground.setVisibility(View.VISIBLE);
                        Animation fadeInAnimation = AnimationUtils.loadAnimation(context, R.anim.fade_in);
                        deskBackground.startAnimation(fadeInAnimation );

                        progressBar.setVisibility(View.GONE);
                        Context context = getApplicationContext();
                        CharSequence text = "Successfully checked into your desk and logged you in";
                        int duration = Toast.LENGTH_LONG;

                        Toast toast = Toast.makeText(context, text, duration);
                        toast.show();
                    }
                    else if(status == 0) {
                        AsyncHttpClient client = new AsyncHttpClient();
                        System.out.println("Tapmo new link: "+(data.toString().replace("status","tabs")));
                        client.get(data.toString().replace("status", "tabs"), new AsyncHttpResponseHandler() {
                            @Override
                            public void onSuccess(String response) {
                                System.out.println("Tapmo status: " + response);
                                Context context = getApplicationContext();
                                CharSequence text = "Opening your computer's chrome tabs";
                                int duration = Toast.LENGTH_LONG;

                                Toast toast = Toast.makeText(context, text, duration);
                                toast.show();

                                Intent i = new Intent(Intent.ACTION_VIEW);
                                i.setData(Uri.parse(response));
                                startActivity(i);
                            }
                        });
                    }
                }
            });
        }
    }
}
