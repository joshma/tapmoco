package com.tapmo;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.widget.TextView;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import java.util.List;

public class MyActivity extends Activity {

    TextView text2;
    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        TextView text = (TextView) findViewById(R.id.text);
        text2 = (TextView) findViewById(R.id.text2);

        Uri data = getIntent().getData();

        if(data != null) {
            List<String> params = data.getPathSegments();
            String first = params.get(1);
            String second = params.get(3);

            text.setText("User: " + first + "\tLocation: "+ second +"\t\tData: " + data.toString());
            AsyncHttpClient client = new AsyncHttpClient();
            client.post(data.toString(), new AsyncHttpResponseHandler() {
                @Override
                public void onSuccess(String response) {
                    text2.setText(response);
                }
            });
        }
    }
}
