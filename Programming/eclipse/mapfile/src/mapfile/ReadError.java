package mapfile;

@SuppressWarnings("serial")
public class ReadError extends Exception {

	public ReadError() {
		super();
	}

	public ReadError(String message) {
		super(message);
	}
}
