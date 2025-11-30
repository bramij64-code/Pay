import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class CreateOrderAPI {

    public static void createOrder() {
        try {
            // OkHttpClient instance
            OkHttpClient client = new OkHttpClient();

            // FormBody Builder for Request
            RequestBody formBody = new FormBody.Builder()
                .add("token_key", "4637a43f8e8db38a97a5d68a110758d3")  // Example token
                .add("secret_key", "40961dcda5338e0cad148a6838fc3dbb") // Example secret
                .add("amount", "1000")
                .add("order_id", "Abc123")
                .add("custumer_mobile", "1234567890")
                .add("redirect_url", "https://zapupi.com/success")
                .add("remark", "TEST")
                .build();

            // Build Request
            Request request = new Request.Builder()
                .url("https://zapupi.com/api/create-order")
                .post(formBody)
                .build();

            // Execute Request
            try (Response response = client.newCall(request).execute()) {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

                // Print Response
                System.out.println("Create Order Response: " + response.body().string());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        createOrder();
    }
}
