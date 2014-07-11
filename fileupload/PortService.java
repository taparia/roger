import java.io.IOException;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class PortService{

	public static void main(String[] args) throws InterruptedException {

		int port = Integer.parseInt(args[0]);

		ServerSocket server = null;
		try {
			server = new ServerSocket(port);
			System.out.println("Server started on port:"+port);
			while(true){
				Socket post;
				post = server.accept();
				String message = "Sample message on port:"+port ;
				OutputStream o=post.getOutputStream();
				o.write(message.getBytes("UTF-8"));
				o.close();
			}

		} catch (IOException e1) {
			System.out.println("Unable to start at port:"+port);
		}
	}
}

