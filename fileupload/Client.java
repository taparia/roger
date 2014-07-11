import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client {
	public static void main(String[] args) throws UnknownHostException, IOException {
		
		int port =Integer.parseInt(args[1]);
		
		Socket socket=new Socket(args[0], port);
		
		InputStream io=socket.getInputStream();
		BufferedReader reader=new BufferedReader(new InputStreamReader(io));
		System.out.println(reader.readLine());
		reader.close();
		io.close();
	}
}

